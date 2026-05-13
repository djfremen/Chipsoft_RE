#!/usr/bin/env python3
"""Chipsoft J2534 USBPcap decoder v2 — separate OUT and IN envelope layouts.

Determined from frame inspection of
2026-05-08-j2534-trioniccanflasher-readecm.pcap:

OUT (queue 0x0022 / commit 0x000F), 35 bytes for 2-byte UDS:
  ofs 0-1   opcode (LE u16)
  ofs 2-5   length (LE u32)
  ofs 6-7   checksum (LE u16)
  ofs 8-11  reserved
  ofs 12-15 protocol (LE u32, 5=CAN)
  ofs 16-19 msgID
  ofs 20-23 txflags
  ofs 24-29 padding zeros
  ofs 30-31 CAN ID (big-endian u16)
  ofs 32    ISO-TP PCI byte
  ofs 33+   UDS data

IN (status 0x2000=MSG_AVAILABLE), 39 bytes for 4-byte UDS:
  ofs 0-1   status (LE u16)
  ofs 2-5   ? (msgID or similar; values look like LE u32 counter)
  ofs 6-9   HARDWARE TIMESTAMP (µs since adapter attach, LE u32) — VERIFIED
  ofs 10-13 protocol (LE u32, 5=CAN)
  ofs 14-17 RxStatus / flags (LE u32, J2534 RX_STATUS bits)
  ofs 18-25 padding / reserved
  ofs 26-27 zeros
  ofs 28-29 CAN ID (big-endian u16)
  ofs 30    ISO-TP PCI byte
  ofs 31+   UDS data

Both forms are PCI-prefixed UDS, NOT raw J2534 PASSTHRU_MSG. Hardware
timestamp on IN side gives µs-resolution per-frame timing.
"""
from __future__ import annotations
import struct, sys
from pathlib import Path
from typing import Iterator, NamedTuple

sys.path.insert(0, "/tmp")
from decode_chipsoft_pcap import iter_usb_frames

# Filter constants
OPCODE_QUEUE   = 0x0022
OPCODE_COMMIT  = 0x000F
STATUS_MSG_AVL = 0x2000   # IN reply when CAN message is available


class UdsExchange(NamedTuple):
    ts_us: int            # USB-receive timestamp (relative to first frame)
    hw_ts_us: int         # device hardware timestamp (relative to attach)
    direction: str        # "TX" or "RX"
    can_id: int
    iso_tp_pci: int
    uds: bytes


def parse_envelope(frame) -> UdsExchange | None:
    p = frame.payload
    if frame.direction == "OUT":
        if len(p) < 33:
            return None
        op = struct.unpack_from("<H", p, 0)[0]
        if op != OPCODE_COMMIT:
            return None  # only emit commit (skip queue dedupe)
        can_id = struct.unpack_from(">H", p, 30)[0]
        pci = p[32]
        uds = p[33:]
        return UdsExchange(frame.ts_us, 0, "TX", can_id, pci, uds)
    else:  # IN
        if len(p) < 32:
            return None
        st = struct.unpack_from("<H", p, 0)[0]
        if st != STATUS_MSG_AVL:
            return None
        hw_ts = struct.unpack_from("<I", p, 6)[0]
        # IN envelope is 1 byte longer in the header than OUT — CAN ID lives
        # at offset 29-30 (BE u16), PCI at 31, UDS at 32+.
        can_id = struct.unpack_from(">H", p, 29)[0]
        pci = p[31]
        uds = p[32:]
        return UdsExchange(frame.ts_us, hw_ts, "RX", can_id, pci, uds)


def decode_uds(uds: bytes) -> str:
    """Use scapy GMLAN if it parses; otherwise show hex."""
    if not uds:
        return "<empty>"
    try:
        import logging
        logging.getLogger("scapy").setLevel(logging.ERROR)
        from scapy.config import conf
        conf.contribs['GMLAN'] = {
            'treat-response-pending-as-answer': True,
            'single_layer_mode': False, 'compatibility_mode': True,
        }
        from scapy.contrib.automotive.gm.gmlan import GMLAN
        pkt = GMLAN(uds)
        # Walk to leaf
        layer = pkt
        names = [layer.name]
        while layer.payload and layer.payload.name not in ("NoPayload", "Raw"):
            layer = layer.payload
            names.append(layer.name)
        fields = []
        for fn in ("securityAccessType", "subFunction", "negativeResponseCode",
                   "service", "dataIdentifier"):
            if hasattr(layer, fn):
                v = getattr(layer, fn)
                if isinstance(v, int):
                    fields.append(f"{fn}=0x{v:02X}")
        return " / ".join(names) + ("  " + " ".join(fields) if fields else "")
    except Exception:
        return f"<{uds[:10].hex(' ')}>"


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("pcap")
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--summary", action="store_true",
                    help="Per-CAN-ID UDS-SID histogram only")
    args = ap.parse_args()

    color = sys.stdout.isatty() and not args.no_color
    counts = {}
    n = 0
    first_hw_ts = None
    for frame in iter_usb_frames(Path(args.pcap)):
        ex = parse_envelope(frame)
        if ex is None:
            continue
        sid = ex.uds[0] if ex.uds else 0
        counts[(ex.direction, ex.can_id, sid)] = counts.get((ex.direction, ex.can_id, sid), 0) + 1

        if not args.summary:
            label = decode_uds(ex.uds)
            pci_kind = {0: "SF", 1: "FF", 2: "CF", 3: "FC"}.get(ex.iso_tp_pci >> 4, "??")
            c = "32" if ex.direction == "RX" else "36"
            if sid == 0x7F: c = "31"
            tag = f"\033[{c}m{ex.direction} ${ex.can_id:04X}\033[0m" if color else f"{ex.direction} ${ex.can_id:04X}"
            ts_ms = ex.ts_us / 1000
            hw = f"hw={ex.hw_ts_us/1000:8.3f}ms" if ex.direction == "RX" else "             "
            hex_uds = ex.uds[:14].hex(" ")
            print(f"[{ts_ms:9.3f}ms {hw}] {tag} [{pci_kind}]  {hex_uds:<42s}  {label}")
        n += 1
        if args.limit and n >= args.limit:
            break

    if args.summary:
        print(f"\n{n} UDS exchanges (commit OUT + msg-available IN)")
        for (d, c, s), v in sorted(counts.items(), key=lambda x: -x[1])[:30]:
            print(f"  {d}  ${c:04X}  SID 0x{s:02X}   ×{v}")


if __name__ == "__main__":
    main()
