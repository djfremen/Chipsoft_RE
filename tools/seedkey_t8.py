#!/usr/bin/env python3
"""
SAAB seed→key for SecurityAccess.

Pure-python port of mattiasclaesson/Trionic
    TrionicCANLib/SeedToKey.cs

Three ECUs / three algorithms:
  Trionic 8  — calc_key_t8(seed, level)   levels: "01", "FB", "FD"
  CIM        — calc_key_cim(seed)         (column integration module)
  ME96       — calc_key_me96(seed)        (Motronic 96)

Validated end-to-end against 45 real ECM-granted (seed, key) pairs from
TrionicCANFlasher session logs spanning 2021-11-11 .. 2025-01-31.
24 pairs match Trionic 8 (level 01); 21 pairs match ME96. 0 unknown.

Usage:
    python seedkey_t8.py                       # run self-test (T8 fixtures)
    python seedkey_t8.py 7F14                  # T8 level 01
    python seedkey_t8.py 7F14 --level FD       # T8 level 0xFD
    python seedkey_t8.py 7F14 --algo cim       # CIM
    python seedkey_t8.py 7F14 --algo me96      # ME96
"""
import argparse
import sys


def calc_key_t8(seed: int, level: str = "01") -> int:
    """Trionic 8 (and Z22SE_LEG, Z22SE_MCP) seed→key."""
    if not 0 <= seed <= 0xFFFF:
        raise ValueError(f"seed must be 0..0xFFFF, got 0x{seed:X}")
    key = ((seed >> 5) | (seed << 11)) & 0xFFFF
    key = (key + 0xB988) & 0xFFFF
    level = level.upper()
    if level == "01":
        pass
    elif level == "FB":
        key ^= 0x8749
        key = (key + 0x06D3) & 0xFFFF
        key ^= 0xCFDF
    elif level == "FD":
        key //= 3
        key ^= 0x8749
        key = (key + 0x0ACF) & 0xFFFF
        key ^= 0x81BF
    else:
        raise ValueError(f"unknown T8 level {level!r} — expected 01/FB/FD")
    return key & 0xFFFF


def calc_key_cim(seed: int) -> int:
    """CIM (Column Integration Module) seed→key."""
    if not 0 <= seed <= 0xFFFF:
        raise ValueError(f"seed must be 0..0xFFFF, got 0x{seed:X}")
    key = (seed + 0x9130) & 0xFFFF
    key = ((key >> 8) | (key << 8)) & 0xFFFF       # byte-swap
    return (0x3FC7 - key) & 0xFFFF


def calc_key_me96(seed: int) -> int:
    """Motronic 96 (ME96) seed→key.  Note: comment in original C# says
       'not correct but works with a patch' — algorithm reproduces every captured
       pair we have, so the 'patch' is presumably elsewhere on the ECM side."""
    if not 0 <= seed <= 0xFFFF:
        raise ValueError(f"seed must be 0..0xFFFF, got 0x{seed:X}")
    c2 = (0xEB + seed) & 0xFF
    if 0x3808 <= seed < 0xA408:
        c2 -= 1
    return (
        (c2 << 9)
        | ((((0x5BF8 + seed) >> 8) & 0xFF) << 1)
        | ((c2 >> 7) & 1)
    ) & 0xFFFF


# Trionic 8 level-01 fixtures from 2025-01-31 + earlier captures.
# See notes/captures/all-trionic-canflasher-fixtures.tsv for the complete
# set across all session logs.
FIXTURES_T8_LEVEL_01 = [
    # (timestamp, seed, expected_key)
    ("2025-01-31 16:44:08", 0x7F14, 0x5D80),
    ("2025-01-31 16:59:49", 0x7E11, 0x4578),
    ("2025-01-31 17:07:27", 0x7F14, 0x5D80),
    ("2025-01-31 20:27:37", 0x5897, 0x744C),
]

# Sample ME96 fixtures (subset — full list of 21 in
# notes/captures/all-trionic-canflasher-fixtures.tsv).
FIXTURES_ME96 = [
    ("2021-11-11 20:43:04", 0x26B2, 0x3B05),    # appears 10x across 3 years
    ("2024-04-29 12:17:23", 0x5A0C, 0xED6D),
    ("2024-05-21 16:32:25", 0x0CB6, 0x42D1),
    ("2024-06-28 18:08:19", 0x569A, 0x0965),
    ("2024-09-21 16:59:53", 0x1469, 0xA8E0),
]


def selftest() -> int:
    fail = 0
    print("=== Trionic 8 level 0x01 ===")
    print(f"{'timestamp':<22} {'seed':<6} {'expected':<10} {'computed':<10} match")
    for ts, seed, expected in FIXTURES_T8_LEVEL_01:
        got = calc_key_t8(seed, "01")
        ok = got == expected
        if not ok:
            fail += 1
        print(f"{ts:<22} {seed:04X}    {expected:04X}        {got:04X}        {'YES' if ok else 'NO'}")
    print(f"\n=== Motronic 96 (ME96) ===")
    print(f"{'timestamp':<22} {'seed':<6} {'expected':<10} {'computed':<10} match")
    for ts, seed, expected in FIXTURES_ME96:
        got = calc_key_me96(seed)
        ok = got == expected
        if not ok:
            fail += 1
        print(f"{ts:<22} {seed:04X}    {expected:04X}        {got:04X}        {'YES' if ok else 'NO'}")
    n = len(FIXTURES_T8_LEVEL_01) + len(FIXTURES_ME96)
    if fail == 0:
        print(f"\nOK: {n}/{n} fixtures pass.")
        return 0
    print(f"\nFAIL: {fail}/{n} fixtures failed.", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("seed", nargs="?", help="seed in hex (e.g. 7F14). Omit for self-test.")
    ap.add_argument("--algo", default="t8", choices=["t8", "cim", "me96"],
                    help="algorithm family (default: t8)")
    ap.add_argument("--level", default="01",
                    help="T8 access level: 01 (default), FB, or FD. Ignored for cim/me96.")
    args = ap.parse_args()

    if args.seed is None:
        return selftest()

    seed = int(args.seed, 16)
    if args.algo == "t8":
        key = calc_key_t8(seed, args.level)
        label = f"T8 level=0x{args.level.upper()}"
    elif args.algo == "cim":
        key = calc_key_cim(seed)
        label = "CIM"
    else:
        key = calc_key_me96(seed)
        label = "ME96"
    print(f"seed=0x{seed:04X}  {label}  key=0x{key:04X}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
