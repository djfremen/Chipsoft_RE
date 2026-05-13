#!/usr/bin/env python3
"""Decode a cstech2win shim log via scapy's GMLAN/UDS dissectors.

The shim records every PDU API call from Tech2Win, including REQ-PDU bytes
(TX to the bus) and RSP-UDS bytes (RX from the bus). Each line looks like:

    1117|13708|HEX  |REQ-PDU|len=7|00 00 02 41 AA 01 01

Fields: ``ms_since_attach``, ``thread_id``, ``HEX``, ``REQ-PDU|RSP-UDS``,
``len``, then the hex payload. The first 4 hex bytes are a chipsoft header
(``00 00 <can_id_hi> <can_id_lo>``); the rest is the UDS payload as Tech2Win
sees it (ISO-TP PCI already stripped by the PDU API).

This tool feeds the UDS slice through scapy's ``GMLAN()`` packet class so
every byte sequence gets a human-readable label: ``SecurityAccessSeedRequest
level=0x0B``, ``NegativeResponse service=0x27 nrc=ResponsePending``, etc.

Usage:
    python3 shim_log_decode.py [log_path]            # decode whole log
    python3 shim_log_decode.py [log_path] --grep 27  # only lines with SID 0x27
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterator, NamedTuple, Optional

# Suppress scapy's interactive banner / warnings.
import logging
logging.getLogger("scapy").setLevel(logging.ERROR)

from scapy.contrib.automotive.gm.gmlan import GMLAN  # noqa: E402
from scapy.contrib.automotive.uds import UDS  # noqa: E402

# Configure GMLAN to treat 0x78 (ResponsePending) as a normal answer so the
# dissector doesn't print a warning every time.
from scapy.config import conf  # noqa: E402
conf.contribs['GMLAN'] = {
    'treat-response-pending-as-answer': True,
    'single_layer_mode': False,
    'compatibility_mode': True,
}

LINE_RE = re.compile(
    r"^(?P<ms>\d+)\|(?P<tid>\d+)\|HEX\s*\|"
    r"(?P<kind>REQ-PDU|RSP-UDS)\|len=(?P<len>\d+)\|(?P<hex>.+)$"
)


class Frame(NamedTuple):
    ms: int
    direction: str  # "TX" or "RX"
    can_id: int
    uds_bytes: bytes


def _parse_line(line: str) -> Optional[Frame]:
    m = LINE_RE.match(line)
    if not m:
        return None
    try:
        raw = bytes.fromhex(m.group("hex").replace(" ", ""))
    except ValueError:
        return None
    if len(raw) < 5:
        return None
    # bytes[0:2] are typically 00 00 (channel/source); bytes[2:4] are CAN
    # ID big-endian; bytes[4:] is the UDS payload (ISO-TP PCI stripped).
    can_id = (raw[2] << 8) | raw[3]
    uds = raw[4:]
    direction = "TX" if m.group("kind") == "REQ-PDU" else "RX"
    return Frame(int(m.group("ms")), direction, can_id, uds)


def iter_frames(log_path: Path) -> Iterator[Frame]:
    """Yield frames from a shim log (one-shot read)."""
    for line in log_path.read_text(errors="replace").splitlines():
        f = _parse_line(line)
        if f is not None:
            yield f


def iter_frames_stdin() -> Iterator[Frame]:
    """Yield frames from stdin, line-buffered. Use with ``tail -F``."""
    for line in sys.stdin:
        f = _parse_line(line.rstrip("\n"))
        if f is not None:
            yield f


def decode_frame(uds_bytes: bytes) -> tuple[str, Optional[GMLAN]]:
    """Return a human label + the scapy packet (or None if undissectable)."""
    if not uds_bytes:
        return "<empty>", None
    try:
        pkt = GMLAN(uds_bytes)
    except Exception as e:  # pragma: no cover — best-effort
        return f"<scapy parse error: {e}>", None

    # scapy dispatches on the service byte; the helpful summary lives in
    # pkt.summary() (e.g. "GMLAN_SA / Raw") and pkt.fields gives us the
    # decoded sub-fields. mysummary() is cleaner when present.
    summary = pkt.mysummary() if hasattr(pkt, "mysummary") else pkt.summary()

    # Walk the layer stack to pull the most informative leaf.
    layer = pkt
    leaf_parts = [layer.name]
    while layer.payload and layer.payload.name != "NoPayload":
        layer = layer.payload
        if layer.name not in ("Raw", "NoPayload"):
            leaf_parts.append(layer.name)
        # Pull noteworthy field values from the leaf layer.
    fields = []
    for fname in ("securityAccessType", "subFunction", "negativeResponseCode",
                  "service", "dataIdentifier", "dataRecord"):
        if hasattr(layer, fname):
            val = getattr(layer, fname)
            if isinstance(val, int):
                fields.append(f"{fname}=0x{val:02X}")
            elif isinstance(val, (bytes, bytearray)) and val:
                fields.append(f"{fname}={bytes(val).hex(' ')}")
    field_str = "  " + " ".join(fields) if fields else ""
    return f"{' / '.join(leaf_parts)}{field_str}", pkt


def _color(text: str, code: str, color_on: bool) -> str:
    if not color_on:
        return text
    return f"\033[{code}m{text}\033[0m"


def _format(frame: Frame, label: str, t_rel: int, color_on: bool) -> str:
    """Pretty-print a frame with ANSI color cues."""
    hex_preview = frame.uds_bytes.hex(" ")[:30]
    sid = frame.uds_bytes[0] if frame.uds_bytes else 0
    if sid == 0x7F:
        col = "31"  # red for NRC
    elif frame.direction == "TX":
        col = "36"  # cyan for TX
    else:
        col = "32"  # green for RX
    # Dim TesterPresent / functional broadcasts so they don't drown signal.
    if frame.can_id == 0x0101 or (sid in (0x3E, 0xFE)):
        col = "2"
    dir_tag = _color(f"{frame.direction} ${frame.can_id:04X}", col, color_on)
    label_col = _color(label, col, color_on)
    return f"[{t_rel:6d}ms] {dir_tag}  {hex_preview:<30}  {label_col}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("log", nargs="?",
                    default="/Users/admin/.openclaw/workspace/Chipsoft_RE/"
                    "shim/cstech2win/captures/"
                    "2026-05-07-shim-v6-seed-deterministic.log",
                    help="path to a shim log, or '-' to read from stdin "
                    "(pair with `tail -F shim.log | ...`)")
    ap.add_argument("--grep", help="only show frames whose hex matches")
    ap.add_argument("--limit", type=int, default=0,
                    help="stop after N frames (0 = all)")
    ap.add_argument("--no-color", action="store_true",
                    help="disable ANSI color output")
    args = ap.parse_args()

    color_on = sys.stdout.isatty() and not args.no_color

    if args.log == "-":
        frames_iter = iter_frames_stdin()
    else:
        log_path = Path(args.log)
        if not log_path.exists():
            sys.exit(f"log not found: {log_path}")
        frames_iter = iter_frames(log_path)

    first_ms = None
    shown = 0
    for f in frames_iter:
        if args.grep and args.grep not in f.uds_bytes.hex():
            continue
        if first_ms is None:
            first_ms = f.ms
        t_rel = f.ms - first_ms
        label, _pkt = decode_frame(f.uds_bytes)
        print(_format(f, label, t_rel, color_on), flush=True)
        shown += 1
        if args.limit and shown >= args.limit:
            break


if __name__ == "__main__":
    main()
