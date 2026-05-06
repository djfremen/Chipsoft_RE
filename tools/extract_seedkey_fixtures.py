#!/usr/bin/env python3
"""
Extract every (seed, key) pair from a directory of TrionicCANFlasher uiLog files,
attribute each to the correct ECU/algorithm, and emit a TSV fixture table.

Usage:
    python extract_seedkey_fixtures.py /path/to/log/dir [-o fixtures.tsv]

Each uiLog line of the form
    "2025-01-31 16:44:08.6893 Security access : Key (5D80) calculated from seed (7F14)"
becomes one fixture row.  The script tries each known algorithm in order and
records which one(s) produce the captured key.
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedkey_t8 import calc_key_t8, calc_key_cim, calc_key_me96

PAIR_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+).*"
    r"Security access : Key \(([0-9A-Fa-f]{4})\) calculated from seed \(([0-9A-Fa-f]{4})\)"
)


def attribute(seed: int, key: int) -> str:
    """Return a comma-separated list of algorithms whose output equals `key`."""
    matches = []
    if calc_key_t8(seed, "01") == key:  matches.append("T8/01")
    if calc_key_t8(seed, "FB") == key:  matches.append("T8/FB")
    if calc_key_t8(seed, "FD") == key:  matches.append("T8/FD")
    if calc_key_cim(seed)     == key:    matches.append("CIM")
    if calc_key_me96(seed)    == key:    matches.append("ME96")
    return ",".join(matches) if matches else "UNKNOWN"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("logdir", help="Directory containing uiLog*.txt files")
    ap.add_argument("-o", "--output", default="-",
                    help="Output TSV path. Default: stdout.")
    args = ap.parse_args()

    pattern = os.path.join(args.logdir, "uiLog*.txt")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No uiLog*.txt files in {args.logdir}", file=sys.stderr)
        return 1

    out = sys.stdout if args.output == "-" else open(args.output, "w")
    out.write("timestamp\tseed_hex\tkey_hex\talgorithm\tsource_file\n")

    counts = {"T8/01": 0, "T8/FB": 0, "T8/FD": 0, "CIM": 0, "ME96": 0, "UNKNOWN": 0}
    for path in files:
        with open(path, "rb") as f:
            text = f.read().decode("latin-1", errors="replace").replace("\x00", " ")
        for ts, key_hex, seed_hex in PAIR_RE.findall(text):
            seed = int(seed_hex, 16)
            key = int(key_hex, 16)
            algo = attribute(seed, key)
            counts[algo.split(",")[0]] = counts.get(algo.split(",")[0], 0) + 1
            out.write(f"{ts}\t{seed:04X}\t{key:04X}\t{algo}\t{os.path.basename(path)}\n")

    if out is not sys.stdout:
        out.close()

    print("\n=== summary ===", file=sys.stderr)
    total = sum(counts.values())
    for k, v in counts.items():
        if v:
            print(f"  {k:>10}: {v}", file=sys.stderr)
    print(f"  {'total':>10}: {total}", file=sys.stderr)
    if args.output != "-":
        print(f"wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
