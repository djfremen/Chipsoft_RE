#!/usr/bin/env python
"""
probe_uds_23.py — Path B sanity probe: send a single UDS $23 ReadMemoryByAddress
to the bench ECM via Chipsoft Pro J2534 and report whether the service is open.

Read-only. Sends $23 only. Never sends $27 — cannot burn the bench's free shot.

================================================================================
BITNESS REQUIREMENT
================================================================================
This script loads `j2534_interface.dll` which is **32-bit (PE32 x86)**. You MUST
run it from a 32-bit Python interpreter, otherwise `WinDLL(...)` fails with
WinError 193.

Install path: download Python 3.x **32-bit** from python.org, then:
    py -3-32 -m pip install --upgrade pip
    py -3-32 tools/win10/probe_uds_23.py

================================================================================
WHAT THIS SCRIPT DOES (default invocation)
================================================================================
1. PassThruOpen     — claim Chipsoft device.
2. PassThruConnect  — open ISO15765 channel @ 500 kbps, 11-bit IDs.
3. PassThruIoctl    — SET_CONFIG to ensure J1962 pin layout matches bench wiring.
4. PassThruStartMsgFilter — flow-control filter for 0x0641 ↔ 0x0241.
5. PassThruWriteMsgs — send the UDS $23 request below.
6. PassThruReadMsgs  — collect the response (J2534's ISO-TP layer reassembles
                       multi-frame responses transparently).
7. Classify the response and print a verdict:
     - 06 63 ...     → service OPEN. Move to Step 2 of Path B (sweep for SSA).
     - 7F 23 33      → SecurityAccessDenied. $23 locked. Pivot to Path A.
     - 7F 23 11      → ServiceNotSupported. Pivot to Path A.
     - 7F 23 31      → RequestOutOfRange. Try a different address; service is
                       open in principle.
     - (no response) → check pin alignment / baud / wiring. See "Bench" below.
8. PassThruDisconnect + PassThruClose.

================================================================================
RUN ORDER
================================================================================
Two probes, neither burns the bench's free shot:

    py -3-32 probe_uds_23.py --id 0x07E0 --baud 500000     # HSCAN OBD-II first
    py -3-32 probe_uds_23.py --id 0x0241 --baud 33333      # SAS-bus second

HSCAN at 0x07E0 first because j2534_interface.dll on this firmware doesn't
expose SWCAN reliably — a SWCAN probe at 0x0241 / 33333 may time out for
bus-reachability reasons that have nothing to do with $23 being supported. If
HSCAN says NotSupported (7F 23 11) or times out clean, the second probe at
0x0241 / 33333 settles whether $23 is gated behind SAS.

The HSCAN path is known good on this bench: this morning's VIN-read returned
5A 90 ... at 0x07E8 over HSCAN 500 k.

================================================================================
EXACT BYTES SENT
================================================================================

UDS payload (default):
    23 14 00 00 00 00 10
    │  │  └────┬────┘ │
    │  │     4-byte   1-byte length = 0x10 (16 bytes)
    │  │     address = 0x00000000
    │  ALFI byte 0x14
    │     · low nibble (0x4) = address size in bytes
    │     · high nibble (0x1) = length size in bytes
    │     · so 0x14 means "4-byte address, 1-byte length"
    │     · `--alfi 0x44` switches to 4+4 (some Trionic 8 dialects)
    SID = $23 ReadMemoryByAddress

Equivalent CAN frame (what the J2534 stack will emit on the wire):
    ID = --id  (default 0x07E0 — OBD-II 11-bit engine request)
    DLC = 8
    Data = 07 23 14 00 00 00 00 10
           │
           └ ISO-TP PCI byte. 0x07 = single-frame, 7 UDS bytes follow.
             Note: the bench-runbook draft shows 06 here; that's a one-byte
             undercount. SID(1) + ALFI(1) + addr(4) + len(1) = 7, so PCI = 0x07.

For ALFI 0x44 the UDS payload becomes 10 bytes — too big for a single frame, so
the J2534 stack will use an ISO-TP first-frame:
    Data = 10 0A 23 44 00 00 00 00   followed by consecutive 21 00 00 10 ...

Expected positive-response framing (16 bytes of data → 17 bytes total UDS
payload of `63 <16 data bytes>`):
    First frame:       10 11 63 D0 D1 D2 D3 D4
    Consecutive frame: 21 D5 D6 D7 D8 D9 DA DB
    Consecutive frame: 22 DC DD DE DF AA AA AA   (last 4 data bytes + padding)

The driver hands these back to PassThruReadMsgs as ONE message with DataSize=17,
Data = 63 <16 bytes>. We do not need to manually reassemble.

================================================================================
WHY ADDRESS 0x000000?
================================================================================
The bench-runbook handoff names three candidate sweep ranges for the SSA:
    0x000000 - 0x010000   boot / config
    0x010000 - 0x020000   IMMO partition (most likely)
    0x020000 - 0x040000   app data

We probe 0x000000 first because:
1. If $23 is locked behind SecurityAccess, the ECM rejects the request whatever
   the address is — we learn that with one request and pivot to Path A.
2. If $23 is open, 0x000000 is the lowest legal address; reading there returns
   *something* (boot vector, RESET stub, or 0xFFs depending on Trionic 8 layout).
   Any non-error response confirms the service works and gives us a ground-truth
   sample to compare against later sweeps.
3. We are NOT expecting the SSA signature (b1 ff ff ff ff ff ff ff ff ff ff ff
   00 01 00 00) at 0x000000. That comes from a sweep, not this probe.

================================================================================
BENCH PRECONDITIONS
================================================================================
- Chipsoft Pro plugged in via USB; Device Manager shows VID 0483 / PID 5740.
- OBD-II cable to bench Trionic 8 ECM; ignition full ON.
- For SAAB engine ECM (SWCAN @ 33.3k on pin 1) consider:
      tools/win10/Set-ChipsoftPinMode.ps1 -Mode SWCAN_PIN1   (registry, restart)
  OR set --baud 33333 below and accept the J2534 J1962_PINS default.
- The default --baud 500000 is HSCAN. The runbook says we should try HSCAN first
  (engine ECM is reachable on HSCAN for some flows even though SAS lives on
  SWCAN). If HSCAN times out, switch to --baud 33333.

================================================================================
HARD RULES
================================================================================
- This script sends $23 only. Do not extend it to fire $27.
- If response is 7F 23 33 (SecAccessDenied), STOP. Do not try to unlock to make
  the probe work — the unlock attempt is the actual unlock and must use the
  one valid key (0x4EED) per the handoff's bench facts.
"""

import argparse
import ctypes
import sys
import time
from ctypes import wintypes


# ---- J2534-1 constants ------------------------------------------------------

PROTOCOL_ISO15765 = 6

# Connect flags
CAN_11BIT_ID = 0x00000000
CAN_29BIT_ID = 0x00000100

# TxFlags
ISO15765_FRAME_PAD = 0x00000040

# IoctlID
SET_CONFIG = 0x01

# SCONFIG ParamIDs
DATA_RATE = 0x01
LOOPBACK = 0x03
J1962_PINS = 0x05

# FilterType
FLOW_CONTROL_FILTER = 3

# Error codes (J2534-1)
STATUS_NOERROR = 0


# ---- J2534-1 structures -----------------------------------------------------

class PASSTHRU_MSG(ctypes.Structure):
    _fields_ = [
        ("ProtocolID", ctypes.c_uint32),
        ("RxStatus", ctypes.c_uint32),
        ("TxFlags", ctypes.c_uint32),
        ("Timestamp", ctypes.c_uint32),
        ("DataSize", ctypes.c_uint32),
        ("ExtraDataIndex", ctypes.c_uint32),
        ("Data", ctypes.c_ubyte * 4128),
    ]


class SCONFIG(ctypes.Structure):
    _fields_ = [("Parameter", ctypes.c_uint32), ("Value", ctypes.c_uint32)]


class SCONFIG_LIST(ctypes.Structure):
    _fields_ = [("NumOfParams", ctypes.c_uint32),
                ("ConfigPtr", ctypes.POINTER(SCONFIG))]


# ---- J2534 wrapper ----------------------------------------------------------

DLL_PATH = r"C:\Program Files (x86)\CHIPSOFT_J2534_Pro_Driver\j2534_interface.dll"


class J2534Error(RuntimeError):
    pass


class J2534:
    def __init__(self, dll_path=DLL_PATH):
        if ctypes.sizeof(ctypes.c_void_p) != 4:
            raise SystemExit(
                "ERROR: this script needs 32-bit Python (j2534_interface.dll "
                "is PE32 x86). Run via:  py -3-32 probe_uds_23.py")
        try:
            self.dll = ctypes.WinDLL(dll_path)
        except OSError as e:
            raise SystemExit(f"ERROR: cannot load {dll_path}: {e}")
        self.h_device = ctypes.c_uint32(0)
        self.h_channel = ctypes.c_uint32(0)

    def _check(self, rc, fn):
        if rc != STATUS_NOERROR:
            err = ctypes.create_string_buffer(80)
            self.dll.PassThruGetLastError(err)
            raise J2534Error(f"{fn} failed (rc={rc}): {err.value.decode(errors='replace')}")

    def open(self):
        rc = self.dll.PassThruOpen(None, ctypes.byref(self.h_device))
        self._check(rc, "PassThruOpen")

    def connect(self, protocol, flags, baud):
        rc = self.dll.PassThruConnect(
            self.h_device, protocol, flags, baud, ctypes.byref(self.h_channel))
        self._check(rc, "PassThruConnect")

    def set_config(self, params):
        cfgs = (SCONFIG * len(params))(
            *(SCONFIG(Parameter=p, Value=v) for p, v in params))
        cfg_list = SCONFIG_LIST(NumOfParams=len(params), ConfigPtr=cfgs)
        rc = self.dll.PassThruIoctl(
            self.h_channel, SET_CONFIG, ctypes.byref(cfg_list), None)
        self._check(rc, "PassThruIoctl(SET_CONFIG)")

    def start_iso15765_filter(self, tx_id, rx_id):
        # mask: match all 11 bits of the ID
        mask = self._mk_msg(_id_bytes(0x07FF))
        pattern = self._mk_msg(_id_bytes(rx_id))
        flow = self._mk_msg(_id_bytes(tx_id))
        h_filter = ctypes.c_uint32(0)
        rc = self.dll.PassThruStartMsgFilter(
            self.h_channel, FLOW_CONTROL_FILTER,
            ctypes.byref(mask), ctypes.byref(pattern), ctypes.byref(flow),
            ctypes.byref(h_filter))
        self._check(rc, "PassThruStartMsgFilter")
        return h_filter.value

    def write(self, tx_id, payload, timeout_ms=200):
        msg = self._mk_msg(_id_bytes(tx_id) + bytes(payload),
                           tx_flags=ISO15765_FRAME_PAD)
        n = ctypes.c_uint32(1)
        rc = self.dll.PassThruWriteMsgs(
            self.h_channel, ctypes.byref(msg), ctypes.byref(n), timeout_ms)
        self._check(rc, "PassThruWriteMsgs")

    def read(self, timeout_ms=2000):
        out = []
        end = time.time() + timeout_ms / 1000.0
        while time.time() < end:
            buf = (PASSTHRU_MSG * 1)()
            n = ctypes.c_uint32(1)
            rc = self.dll.PassThruReadMsgs(
                self.h_channel, buf, ctypes.byref(n),
                max(1, int((end - time.time()) * 1000)))
            if rc != STATUS_NOERROR:
                # ERR_BUFFER_EMPTY (0x10) is the timeout case
                if rc == 0x10:
                    break
                self._check(rc, "PassThruReadMsgs")
            for i in range(n.value):
                m = buf[i]
                # ISO15765 messages prefix Data with a 4-byte ID. Strip it.
                if m.DataSize >= 4:
                    out.append(bytes(m.Data[4:m.DataSize]))
                # The first response after a write is the TxDone echo
                # (RxStatus & TX_MSG_TYPE). Skip it — caller handles via len.
        return out

    def disconnect(self):
        if self.h_channel.value:
            self.dll.PassThruDisconnect(self.h_channel)
            self.h_channel = ctypes.c_uint32(0)

    def close(self):
        if self.h_device.value:
            self.dll.PassThruClose(self.h_device)
            self.h_device = ctypes.c_uint32(0)

    @staticmethod
    def _mk_msg(data, tx_flags=0):
        m = PASSTHRU_MSG(ProtocolID=PROTOCOL_ISO15765, TxFlags=tx_flags,
                         DataSize=len(data))
        for i, b in enumerate(data):
            m.Data[i] = b
        return m


def _id_bytes(can_id):
    # ISO15765 messages on J2534 prefix the payload with a 4-byte big-endian ID.
    return can_id.to_bytes(4, "big")


# ---- UDS request builder ----------------------------------------------------

def build_read_memory(addr, length, alfi):
    """Build the UDS $23 ReadMemoryByAddress payload.

    ALFI byte:
        low nibble  = address size in bytes  (0x4 → 4-byte address)
        high nibble = length size in bytes   (0x1 → 1-byte length)
    """
    addr_size = alfi & 0x0F
    len_size = (alfi >> 4) & 0x0F
    if addr_size == 0 or len_size == 0:
        raise ValueError(f"ALFI 0x{alfi:02X} has zero-size field")
    return (bytes([0x23, alfi])
            + addr.to_bytes(addr_size, "big")
            + length.to_bytes(len_size, "big"))


def classify(rsp):
    if not rsp:
        return ("NO_RESPONSE",
                "ECM did not reply within timeout. Check pin alignment, baud, "
                "wiring, ignition, ECM power.")
    b = rsp[0]
    if len(b) >= 1 and b[0] == 0x63:
        return ("OPEN", f"$23 returned positive response, {len(b)-1} data bytes. "
                f"Service is open. Sweep for SSA signature next.")
    if len(b) >= 3 and b[0] == 0x7F and b[1] == 0x23:
        nrc = b[2]
        nrc_map = {
            0x11: ("NOT_SUPPORTED",
                   "ServiceNotSupported. ECM doesn't expose $23. Pivot to Path A."),
            0x12: ("SUBFUNC_NOT_SUPPORTED",
                   "SubFunctionNotSupported."),
            0x13: ("INVALID_FORMAT",
                   "IncorrectMessageLengthOrInvalidFormat. Try ALFI 0x44 (4+4)."),
            0x22: ("CONDITIONS_NOT_CORRECT",
                   "ConditionsNotCorrect. ECM may need session change first."),
            0x31: ("OUT_OF_RANGE",
                   "RequestOutOfRange. Service open but address invalid; "
                   "try a different address (the SSA is likely 0x010000+)."),
            0x33: ("LOCKED",
                   "SecurityAccessDenied. $23 is gated behind SecurityAccess. "
                   "Pivot to Path A. DO NOT try to unlock to probe further."),
            0x35: ("INVALID_KEY",
                   "InvalidKey. Should not appear for a $23 probe."),
            0x36: ("EXCEEDED_ATTEMPTS",
                   "ExceededNumberOfAttempts."),
            0x37: ("LOCKOUT",
                   "RequiredTimeDelayNotExpired. ECM is in 10s lockout — wait."),
            0x78: ("PENDING",
                   "ResponsePending. Reissue read with longer timeout."),
        }
        verdict, msg = nrc_map.get(
            nrc, (f"NRC_0x{nrc:02X}", f"Negative response, NRC=0x{nrc:02X}."))
        return (verdict, msg)
    return ("UNEXPECTED",
            f"Unexpected response shape: {b.hex(' ')}. Investigate.")


# ---- main -------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--addr", default="0x000000",
                    help="Memory address to read (default: 0x000000)")
    ap.add_argument("--len", dest="length", type=lambda s: int(s, 0),
                    default=16, help="Number of bytes to read (default: 16)")
    ap.add_argument("--alfi", default="0x14",
                    help="ALFI byte: 0x14 = 4-byte addr + 1-byte len (default), "
                         "0x44 = 4+4")
    ap.add_argument("--id", "--tx-id", dest="tx_id", default="0x07E0",
                    help="Tester→ECU CAN ID (default: 0x07E0 — OBD-II engine "
                         "request, 11-bit). Use 0x0241 for SAAB physical "
                         "engine-ECM addressing.")
    ap.add_argument("--rx-id", default=None,
                    help="ECU→tester CAN ID. If unset, auto-derived from --id: "
                         "0x07E0..0x07E7 → +0x008 (OBD-II), else +0x400 (SAAB).")
    ap.add_argument("--baud", type=int, default=500000,
                    help="CAN baud (500000 HSCAN [default], 33333 SWCAN)")
    ap.add_argument("--j1962-pins", type=lambda s: int(s, 0), default=0,
                    help="J1962_PINS SET_CONFIG value (default 0 = leave to driver)")
    ap.add_argument("--timeout-ms", type=int, default=2000,
                    help="Read timeout (default 2000 ms)")
    args = ap.parse_args()

    addr = int(args.addr, 0)
    alfi = int(args.alfi, 0)
    tx_id = int(args.tx_id, 0)
    if args.rx_id is None:
        rx_id = tx_id + (0x008 if 0x07E0 <= tx_id <= 0x07E7 else 0x400)
    else:
        rx_id = int(args.rx_id, 0)

    uds = build_read_memory(addr, args.length, alfi)
    print(f"=== Path B $23 probe ===")
    print(f"  TX/RX CAN IDs : 0x{tx_id:04X} / 0x{rx_id:04X}")
    print(f"  Baud          : {args.baud}")
    print(f"  ALFI          : 0x{alfi:02X}")
    print(f"  Address       : 0x{addr:08X}")
    print(f"  Length        : {args.length}")
    print(f"  UDS payload   : {uds.hex(' ')} ({len(uds)} bytes)")
    print()

    j = J2534()
    try:
        j.open()
        j.connect(PROTOCOL_ISO15765, CAN_11BIT_ID, args.baud)

        cfg = [(LOOPBACK, 0)]
        if args.j1962_pins:
            cfg.append((J1962_PINS, args.j1962_pins))
        j.set_config(cfg)

        j.start_iso15765_filter(tx_id, rx_id)
        j.write(tx_id, uds)
        rsp = j.read(timeout_ms=args.timeout_ms)
    finally:
        j.disconnect()
        j.close()

    print(f"=== Response ===")
    if not rsp:
        print("  (no frames)")
    for i, frame in enumerate(rsp):
        print(f"  [{i}] {frame.hex(' ')}")
    print()
    verdict, msg = classify(rsp)
    print(f"=== Verdict: {verdict} ===")
    print(f"  {msg}")
    return 0 if verdict in ("OPEN", "OUT_OF_RANGE") else 1


if __name__ == "__main__":
    sys.exit(main())
