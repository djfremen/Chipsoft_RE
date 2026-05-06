# SAAB seed→key — algorithms verified at scale

**Source data:** 26 TrionicCANFlasher uiLog files spanning 2021-11-11 through
2025-01-31. Logs are local (~/Desktop/logs_from_trionic/, 751 MB). Extraction
is reproducible from the logs via `tools/extract_seedkey_fixtures.py`; the
extracted fixture table lives at `notes/captures/all-trionic-canflasher-fixtures.tsv`.

**Algorithms:** ported from
[mattiasclaesson/Trionic](https://github.com/mattiasclaesson/Trionic)
`TrionicCANLib/SeedToKey.cs` to `tools/seedkey_t8.py`.

## Result: 45 / 45 captured pairs accounted for

| Algorithm        | Pairs | Validates |
|------------------|-------|-----------|
| Trionic 8, level 0x01 | 24    | ✅       |
| Motronic 96 (ME96)    | 21    | ✅       |
| **Unknown / unmatched** | **0** | —      |

Every captured (seed, key) pair across **3+ years of sessions** matches one of
the documented `SeedToKey.cs` algorithms. Both the Trionic 8 path and the ME96
path are bit-for-bit confirmed.

## The algorithms

```python
# Trionic 8 (level 0x01 — used for engine ECM SecurityAccess)
key = (ror16(seed, 5) + 0xB988) mod 2^16

# Motronic 96
c2 = (0xEB + seed) & 0xFF
if 0x3808 <= seed < 0xA408:
    c2 -= 1
key = ((c2 << 9) | ((((0x5BF8 + seed) >> 8) & 0xFF) << 1) | ((c2 >> 7) & 1)) & 0xFFFF
```

Both are trivial to port to any language.

## Determinism evidence — strong

For every observed (level, seed) tuple, the captured key was always identical.
**No collisions across the entire 45-pair dataset.** Same (seed, level) →
always same key.

This is what we'd expect from a deterministic algorithm — but it also means
that for any given ECU **the seed→key mapping is a fixed function**. There is
no per-session randomness in the key derivation.

## Determinism evidence — seeds repeat across years

Even more striking: the *seeds themselves* repeat across sessions years apart.

| Seed   | Times observed | First seen          | Last seen           | Algorithm |
|--------|----------------|---------------------|---------------------|-----------|
| 0x26B2 | **10**         | 2021-11-11 20:43:04 | 2024-05-09 12:22:25 | ME96      |
| 0x7D45 | 9              | 2024-10-06 14:43:30 | 2024-10-06 15:33:49 | ME96      |
| 0x5A0C | 4              | 2024-04-29 12:17:23 | 2024-05-09 11:53:15 | ME96      |
| 0x569A | 3              | 2024-06-28 18:08:19 | 2024-07-02 13:24:24 | ME96      |
| 0x9A1E | 2              | 2024-07-12 15:15:17 | 2024-07-12 15:22:23 | ME96      |
| 0x7F14 | 2              | 2025-01-31 16:44:08 | 2025-01-31 17:07:27 | T8/01     |

Seed 0x26B2 alone appeared 10 times across nearly 3 years — different days,
different power cycles, different module operations. The ECM either:
1. Has a small, deterministic seed pool (perhaps backed by a fixed-position
   counter or stable register), OR
2. Uses a true PRNG with very rare state changes between auth attempts, OR
3. Hashes some near-stable input (e.g., a calibration-region-derived value)
   to a small output space

**Implications for the Android-direct unlock path**: nothing changes — we
always derive the key live from the seed.

**Implications for replay scenarios** (informational, not a goal): if seeds
genuinely cluster around stable values for a given ECM, then a previously
captured (seed, key) pair may statistically be reusable on a future auth
attempt against the same ECM. This is a non-trivial security observation
that's worth recording for threat-modeling discussions; we are not pursuing
it for our own work.

## Reproducing locally

```bash
# Extract every (seed, key) pair from a directory of uiLog files.
python tools/extract_seedkey_fixtures.py /path/to/logs_from_trionic -o fixtures.tsv

# Run the bundled self-test against fixed fixtures (no log files needed).
python tools/seedkey_t8.py

# Compute a key for a specific seed (any algorithm).
python tools/seedkey_t8.py 7F14
python tools/seedkey_t8.py 26B2 --algo me96
python tools/seedkey_t8.py 7F14 --level FD
```

## Adapter context

The captured sessions used various adapters across years; the 2025-01-31
session (the seed for this analysis) used an ELM327-based adapter
(`CANELM327Device` in stack traces, `selectedIndex=2`). Algorithm validation
is transport-independent, so all captures are valid regardless of adapter.

## What this unlocks

- ✅ **Algorithm port to Kotlin is safe** — Trionic 8 path (24 fixtures) and
     ME96 path (21 fixtures) both validated against years of real ECM
     responses.
- ✅ **Determinism is established** — same (seed, level) → same key, always.
- ⏳ **Bench capture (Tech2 sequence + ISO-TP details + CANHacker pin-1
     question)** is still useful for the *transport* layer; it's no longer a
     blocker for the key-derivation layer.
