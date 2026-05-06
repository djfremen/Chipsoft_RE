#!/usr/bin/env python3
"""
SAAB Trionic 8 SecurityAccess — seed→key.

Pure-python port of mattiasclaesson/Trionic
    TrionicCANLib/SeedToKey.cs::calculateKey()

Verified against four real ECM-granted (seed, key) pairs captured by
TrionicCANFlasher v0.1.73.0 against a Trionic 8 ECU (2025-01-31, session log
in notes/captures/2025-01-31-trionic-canflasher-uilog.txt). All four match.

Levels:
  AccessLevel01  — used by all four captured fixtures; default for engine ECM
  AccessLevelFB  — alternate; XOR + add cascade
  AccessLevelFD  — highest; div-3 + XOR + add cascade

Usage:
    python seedkey_t8.py                       # run self-test against fixtures
    python seedkey_t8.py 7F14                  # compute key for seed (level 01)
    python seedkey_t8.py 7F14 --level FD       # level 0xFD
"""
import argparse
import sys


def calc_key_t8(seed: int, level: str = "01") -> int:
    """Compute the 16-bit Trionic 8 key for a 16-bit seed at the given level.

    level: "01" | "FB" | "FD" (case-insensitive)
    """
    if not 0 <= seed <= 0xFFFF:
        raise ValueError(f"seed must be 0..0xFFFF, got 0x{seed:X}")

    # 16-bit rotate-right by 5, then add 0xB988 (mod 2^16)
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
        raise ValueError(f"unknown level {level!r} — expected 01 / FB / FD")

    return key & 0xFFFF


# Captured (seed, key) pairs from a real ECM session — see header docstring.
FIXTURES_LEVEL_01 = [
    # (timestamp, seed, expected_key)
    ("2025-01-31 16:44:08", 0x7F14, 0x5D80),
    ("2025-01-31 16:59:49", 0x7E11, 0x4578),
    ("2025-01-31 17:07:27", 0x7F14, 0x5D80),  # duplicate seed of pair #1 — see notes
    ("2025-01-31 20:27:37", 0x5897, 0x744C),
]


def selftest() -> int:
    print(f"{'timestamp':<22} {'seed':<6} {'expected':<10} {'computed':<10} match")
    fail = 0
    for ts, seed, expected in FIXTURES_LEVEL_01:
        got = calc_key_t8(seed, "01")
        ok = got == expected
        if not ok:
            fail += 1
        print(f"{ts:<22} {seed:04X}    {expected:04X}        {got:04X}        {'YES' if ok else 'NO'}")
    print()
    if fail == 0:
        print(f"OK: {len(FIXTURES_LEVEL_01)}/{len(FIXTURES_LEVEL_01)} fixtures pass.")
        return 0
    print(f"FAIL: {fail}/{len(FIXTURES_LEVEL_01)} fixtures failed.", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("seed", nargs="?",
                    help="seed in hex (e.g. 7F14). Omit to run self-test.")
    ap.add_argument("--level", default="01", choices=["01", "FB", "FD", "01", "fb", "fd"],
                    help="access level (default: 01)")
    args = ap.parse_args()

    if args.seed is None:
        return selftest()

    seed = int(args.seed, 16)
    key = calc_key_t8(seed, args.level)
    print(f"seed=0x{seed:04X}  level=0x{args.level.upper()}  key=0x{key:04X}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
