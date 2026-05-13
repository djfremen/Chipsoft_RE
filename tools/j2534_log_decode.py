#!/usr/bin/env python3
"""Decode a j2534_interface shim log via scapy's GMLAN/UDS dissectors.

Sister of shim_log_decode.py. The j2534 shim's log format is richer
than the cstech2win shim because the J2534 API exposes more semantic
fields per message (ProtocolID, RxStatus, TxFlags, hardware Timestamp).

Each line:
    <ms_since_attach> | <wall_clock_ms> | <tid> | <event> | <fn> | <detail>

Hex payload lines look like:
    1234|1715661234567|7890|HEX  |TX[0]|len=2|27 01

Usage:
    python3 j2534_log_decode.py [log_path]
    python3 j2534_log_decode.py [log_path] --grep 27
"""
from __future__ import annotations
import argparse, re, sys, logging
from pathlib import Path
from typing import Iterator, NamedTuple

logging.getLogger("scapy").setLevel(logging.ERROR)
from scapy.contrib.automotive.gm.gmlan import GMLAN  # noqa: E402
from scapy.config import conf  # noqa: E402
conf.contribs['GMLAN'] = {
    'treat-response-pending-as-answer': True,
    'single_layer_mode': False, 'compatibility_mode': True,
}

LINE_RE = re.compile(
    r"^(?P<ms>\d+)\|(?P<wall>\d+)\|(?P<tid>\d+)\|"
    r"(?P<event>\w+\s*)\|(?P<fn>[^|]+)\|(?P<detail>.*)$"
)
HEX_TAIL_RE = re.compile(r"len=(\d+)\|(.+)$")


class Frame(NamedTuple):
    ms: int
    wall_ms: int
    tid: int
    event: str
    fn: str
    detail: str


def iter_frames(path: Path) -> Iterator[Frame]:
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith("#"):
            continue
        m = LINE_RE.match(line)
        if not m:
            continue
        yield Frame(int(m["ms"]), int(m["wall"]), int(m["tid"]),
                    m["event"].strip(), m["fn"].strip(), m["detail"].strip())


def decode_uds(hex_str: str) -> str:
    raw = bytes.fromhex(hex_str.replace(" ", ""))
    if not raw:
        return "<empty>"
    try:
        pkt = GMLAN(raw)
        layer = pkt
        names = [layer.name]
        while layer.payload and layer.payload.name not in ("NoPayload", "Raw"):
            layer = layer.payload
            names.append(layer.name)
        fields = []
        for fn in ("securityAccessType", "subFunction",
                   "negativeResponseCode", "service", "dataIdentifier"):
            if hasattr(layer, fn):
                v = getattr(layer, fn)
                if isinstance(v, int):
                    fields.append(f"{fn}=0x{v:02X}")
        return " / ".join(names) + ("  " + " ".join(fields) if fields else "")
    except Exception:
        return f"<{raw[:10].hex(' ')}>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--grep", help="filter by substring in detail or hex")
    ap.add_argument("--no-color", action="store_true")
    args = ap.parse_args()
    color = sys.stdout.isatty() and not args.no_color
    p = Path(args.log)
    first_ms = None
    for f in iter_frames(p):
        if first_ms is None:
            first_ms = f.ms
        t_rel = f.ms - first_ms
        # HEX lines have payload after len=N|
        hex_m = HEX_TAIL_RE.search(f.detail) if f.event == "HEX" else None
        if hex_m and f.fn.startswith(("TX", "RX")):
            hex_str = hex_m.group(2)
            label = decode_uds(hex_str)
            tag = f"{f.fn:<8}"
            c = "32" if f.fn.startswith("RX") else "36"
            if hex_str.replace(" ", "").startswith("7f"):
                c = "31"
            if color:
                print(f"[{t_rel:6d}ms] \033[{c}m{tag} {hex_str:<30s}  {label}\033[0m")
            else:
                print(f"[{t_rel:6d}ms] {tag} {hex_str:<30s}  {label}")
        elif args.grep:
            if args.grep in f.detail:
                print(f"[{t_rel:6d}ms] {f.event:<5} {f.fn:<22} {f.detail}")
        else:
            print(f"[{t_rel:6d}ms] {f.event:<5} {f.fn:<22} {f.detail}")


if __name__ == "__main__":
    main()
