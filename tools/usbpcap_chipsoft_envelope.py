#!/usr/bin/env python3
"""Decode a Chipsoft J2534 USBPcap into a chronological UDS timeline.

Source format: USBPcap link-type 249 (0xF9). Each link record is a
USBPCAP_BUFFER_PACKET_HEADER followed by USB transfer data:

  uint16  headerLen
  uint64  irpId
  uint32  status
  uint16  function
  uint8   info        # bit 0 = transfer direction
  uint16  bus
  uint16  device
  uint8   endpoint    # 0x80 bit = IN (device → host)
  uint8   transfer    # 3 = BULK
  uint32  dataLength
  ...                 # per-transfer extras (none for BULK)
  data[dataLength]

Chipsoft envelope on bulk endpoints (0x01 OUT, 0x81 IN), confirmed
from prior pcap mining (notes/pcap-mining/2026-05-11-...md):

  ofs 0-1     opcode      0x0022 = queue, 0x000F = commit, 0x0024 = IN reply
  ofs 2-5     length      LE u32 (= total envelope len - 8)
  ofs 6-7     checksum    body-dependent
  ofs 8-11    reserved
  ofs 12-15   protocol    LE u32 (5 = CAN, 6 = ISO15765 etc.)
  ofs 16-19   msgID       0 in queue, chipsoft-assigned in commit / IN
  ofs 20-23   txflags
  ofs 24-29   padding
  ofs 30-31   CAN ID      big-endian 16-bit
  ofs 32      ISO-TP PCI  Single Frame: 0x0X (X = UDS bytes)
                          First Frame:  0x1X XX (X = total UDS len)
                          Consec Frame: 0x2N (N = sequence)
  ofs 33+     UDS bytes
"""
from __future__ import annotations
import struct
import sys
from pathlib import Path
from typing import Iterator, NamedTuple

PCAP_GLOBAL_HEADER_LEN = 24
PCAP_RECORD_HEADER_LEN = 16  # ts_sec, ts_usec, incl_len, orig_len


class UsbFrame(NamedTuple):
    ts_us: int            # microseconds since first frame
    direction: str        # "OUT" or "IN"
    endpoint: int         # 0x01 or 0x81
    payload: bytes        # USB transfer payload (chipsoft envelope + data)


def iter_usb_frames(path: Path) -> Iterator[UsbFrame]:
    """Stream USB frames out of a USBPcap pcap file."""
    with path.open("rb") as f:
        gh = f.read(PCAP_GLOBAL_HEADER_LEN)
        if len(gh) < PCAP_GLOBAL_HEADER_LEN:
            return
        magic = gh[:4]
        if magic not in (b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4"):
            raise SystemExit(f"not a pcap file: {path}")
        first_ts: int | None = None
        while True:
            rh = f.read(PCAP_RECORD_HEADER_LEN)
            if len(rh) < PCAP_RECORD_HEADER_LEN:
                return
            ts_sec, ts_usec, incl_len, _orig = struct.unpack("<IIII", rh)
            data = f.read(incl_len)
            if len(data) < incl_len:
                return
            ts_us_abs = ts_sec * 1_000_000 + ts_usec
            if first_ts is None:
                first_ts = ts_us_abs
            ts_us = ts_us_abs - first_ts

            # USBPcap header
            if len(data) < 27:
                continue
            (header_len,) = struct.unpack_from("<H", data, 0)
            if header_len > len(data):
                continue
            # endpoint at offset 21, transfer at 22, dataLength at 23
            endpoint = data[21]
            transfer = data[22]
            (data_len,) = struct.unpack_from("<I", data, 23)
            if transfer != 3:  # only BULK
                continue
            payload = data[header_len:header_len + data_len]
            if not payload:
                continue
            direction = "IN" if endpoint & 0x80 else "OUT"
            yield UsbFrame(ts_us, direction, endpoint, payload)


# Chipsoft envelope decoder
class ChipsoftMsg(NamedTuple):
    ts_us: int
    direction: str        # "TX" (host queues + commits) or "RX" (chipsoft IN)
    opcode: int
    can_id: int
    uds: bytes            # raw UDS bytes after ISO-TP PCI byte
    iso_tp_pci: int       # PCI byte (0x0X = SF, 0x1X = FF, 0x2X = CF)
    msg_id: int
    proto: int


def decode_envelope(frame: UsbFrame) -> ChipsoftMsg | None:
    p = frame.payload
    if len(p) < 33:
        return None
    opcode = struct.unpack_from("<H", p, 0)[0]
    proto = struct.unpack_from("<I", p, 12)[0]
    msg_id = struct.unpack_from("<I", p, 16)[0]
    can_id = struct.unpack_from(">H", p, 30)[0]
    pci = p[32]
    uds_payload = p[33:]
    if frame.direction == "OUT":
        # Queue (0x22) + commit (0x0F) — we keep both but mark commit.
        kind = "TX"
    else:
        kind = "RX"
    return ChipsoftMsg(
        ts_us=frame.ts_us, direction=kind, opcode=opcode, can_id=can_id,
        uds=uds_payload, iso_tp_pci=pci, msg_id=msg_id, proto=proto,
    )


def render(msg: ChipsoftMsg, color: bool) -> str:
    sid = msg.uds[0] if msg.uds else 0
    op_label = {0x0022: "Q", 0x000F: "C", 0x0024: "R"}.get(msg.opcode, f"?{msg.opcode:04X}")
    if msg.direction == "TX":
        if op_label == "Q":
            return ""  # we'll render commit only to dedupe
        c = "36"  # cyan TX
    else:
        c = "32"  # green RX
    if sid == 0x7F:
        c = "31"  # red NRC
    if msg.can_id == 0x0101 or sid in (0x3E, 0xFE):
        c = "2"
    pci_kind = {0: "SF", 1: "FF", 2: "CF"}.get(msg.iso_tp_pci >> 4, "??")
    hex_uds = msg.uds[:14].hex(" ")
    if color:
        tag = f"\033[{c}m{msg.direction:<2} ${msg.can_id:04X}\033[0m"
        op = f"\033[{c}m[{op_label}/{pci_kind}]\033[0m"
    else:
        tag = f"{msg.direction:<2} ${msg.can_id:04X}"
        op = f"[{op_label}/{pci_kind}]"
    ts_ms = msg.ts_us / 1000
    return f"[{ts_ms:9.3f}ms] {tag} {op}  {hex_uds}"


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("pcap", help="USBPcap file")
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("--with-queues", action="store_true",
                    help="Show 'queue' frames in addition to 'commit' frames "
                    "(default: dedupe, show commit only)")
    ap.add_argument("--summary", action="store_true",
                    help="Print only a per-CAN-ID summary at the end")
    args = ap.parse_args()
    color = sys.stdout.isatty() and not args.no_color

    counts = {}        # (direction, can_id, sid) -> count
    seen_commit = set()  # to dedupe queue + commit
    n = 0
    for frame in iter_usb_frames(Path(args.pcap)):
        msg = decode_envelope(frame)
        if msg is None:
            continue
        # Skip queue (Q) frames if commit will follow — but commit is the "real" send
        if not args.with_queues and msg.direction == "TX" and msg.opcode == 0x0022:
            continue
        sid = msg.uds[0] if msg.uds else 0
        counts[(msg.direction, msg.can_id, sid)] = counts.get((msg.direction, msg.can_id, sid), 0) + 1
        if not args.summary:
            line = render(msg, color)
            if line:
                print(line)
        n += 1
    if args.summary:
        print(f"\n{n} chipsoft frames")
        print("\n(direction, can_id, sid) → count:")
        for (d, c, s), v in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"  {d}  ${c:04X}  SID 0x{s:02X}   ×{v}")


if __name__ == "__main__":
    main()
