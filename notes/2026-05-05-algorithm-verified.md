# Trionic 8 SecurityAccess seed→key — algorithm verified

**Source data:** TrionicCANFlasher v0.1.73.0 uiLog from a 2025-01-31 session on a real
SAAB Trionic 8 ECU. Saved at `notes/captures/2025-01-31-trionic-canflasher-uilog.txt`.

**Algorithm:** ported from [mattiasclaesson/Trionic](https://github.com/mattiasclaesson/Trionic)
`TrionicCANLib/SeedToKey.cs`. Implemented at `tools/seedkey_t8.py`.

For AccessLevel01:
```
key = ror16(seed, 5) + 0xB988    (mod 2^16)
```

That's it — 16-bit rotate-right by 5, add a constant. Trivial to port to Kotlin or any
other target.

## Verified pairs (level 0x01)

| Timestamp           | Seed   | Expected | Computed | Match |
|---------------------|--------|----------|----------|-------|
| 2025-01-31 16:44:08 | 0x7F14 | 0x5D80   | 0x5D80   | ✅    |
| 2025-01-31 16:59:49 | 0x7E11 | 0x4578   | 0x4578   | ✅    |
| 2025-01-31 17:07:27 | 0x7F14 | 0x5D80   | 0x5D80   | ✅    |
| 2025-01-31 20:27:37 | 0x5897 | 0x744C   | 0x744C   | ✅    |

All four pairs were granted by the ECM in the captured session ("Security access
granted" in the log). The algorithm matches every one.

## Side observation: seeds repeat

Pair #1 (16:44) and pair #3 (17:07) have **identical seeds (0x7F14)** ~23 minutes apart.
This implies SAAB Trionic 8 SecurityAccess seeds are **not pure session-nonces** — they
appear to be derived from some deterministic state in the ECM. Possible mechanisms:

1. ECM uses a PRNG that doesn't tick except on explicit auth attempts, and pairs #1 and
   #3 came from a state where the PRNG was in the same position
2. ECM had been power-cycled to the same boot state between #2 and #3
3. Seed is genuinely deterministic from some stable ECM state and not nonce-based at all

**Implications:**
- For our **Android-direct unlock path**, this doesn't change anything — we always
  derive the key from the seed at runtime, so deterministic-or-nonce-doesn't-matter.
- For **replay-based attacks** (capture old (seed, key), replay key), determinism would
  make this viable in some scenarios. We're not pursuing replay, but worth noting for
  threat modeling.

This is one captured session; would need more data to firm up the conjecture.

## What this unlocks

Algorithm verification was the gating step in the bench-capture-plan
(`notes/2026-05-05-bench-capture-plan.md`). With this in hand:

- ✅ Kotlin port of `seedkey_t8.py` is safe — algorithm matches real ECM behavior
- ✅ Don't need to do additional bench captures just for algorithm validation
- ⏳ Still want a bench capture for: Tech2's exact UDS sequence (session-control,
     TesterPresent cadence, ISO-TP framing on SWCAN @ 33.3k), and confirmation that
     CANHacker mode on the Chipsoft sees pin 1. Both are independent of this finding.

## Adapter used in the captured session

The log shows `CANELM327Device` in a stack trace at line 778-780, with
`selectedIndex=2` in `ITrionic.GetAdapterNames`. So the captured session used an
**ELM327-based adapter** — likely a clone with at least basic GMLAN support. Worth
noting because:
- ELM327 doesn't natively support SWCAN; either the bus was HSCAN, or this is a modded
  adapter (some clones have GMLAN firmware)
- The seed→key algorithm is independent of transport, so the captured pairs are valid
  regardless

## Reproducing locally

```bash
python tools/seedkey_t8.py            # runs self-test against the 4 fixtures
python tools/seedkey_t8.py 7F14       # compute key for any seed (level 01 default)
python tools/seedkey_t8.py 7F14 --level FD
```
