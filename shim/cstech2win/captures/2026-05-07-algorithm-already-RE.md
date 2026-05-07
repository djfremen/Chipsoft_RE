# 2026-05-07 — algorithm is already RE'd; project pivots from "extract algo" to "decode SSA"

After capturing the first `$27 $0B` seed (`0xC4DC`) and confirming it's deterministic across two cold runs, we went looking for historical seed/key data to start RE'ing the algorithm. **It turned out the algorithm has been reverse-engineered for some time** — sitting in `saab_security_project/SAABSecurityAccess/python_server/security_calc.py` (1023 lines, 2609-byte data table; header literally says "Reverse-engineered from dllsecurity.dll").

## Validation

Ran `security_calc.get_key_from_seed(seed, algo)` against all 12 ground-truth `(algo, seed, key)` tuples from `~/Desktop/tis2web_logs/ground_truth.md` (HWKID `Q000000010`, SAS server output for a real Tech2 session):

```
algo    seed    expected_key   computed   result
0x366   0x3949  0x8249      →  0x8249     OK
0x361   0xDA34  0x4100      →  0x4100     OK
0x365   0xF428  0xE742      →  0xE742     OK
0x339   0xAD0A  0x0EF0      →  0x0EF0     OK
0x339   0x6D82  0xCCF4      →  0xCCF4     OK
0x360   0x5AEF  0x1FC8      →  0x1FC8     OK
0x30B   0x0191  0xF8BA      →  0xF8BA     OK
0x339   0x07C2  0xC9C6      →  0xC9C6     OK
0x339   0x3882  0xCB4C      →  0xCB4C     OK
0x339   0x2E25  0xE2F9      →  0xE2F9     OK
0x32F   0xD0CB  0x994F      →  0x994F     OK
0x367   0x7A92  0xAA49      →  0xAA49     OK

12/12 match.
```

The function uses an "Alt1" lookup table (one of three tables built into `security_calc.py`) and is universal across all SAAB ECMs — only the (algo, seed) pair changes per ECU.

## SSA card layout (verified against `bojer_ssa.bin`)

The SSA card stores 12 SKA tuples in a fixed block:

```
offset 0x00:        magic 0xB1 0x00
offset 0x02-0x0B:   HWKID (10 ASCII bytes)
offset 0x0C-0x0D:   SSA version (2B BE)
offset 0x0E-0x0F:   free shots / status
offset 0x14:        VIN tuples block (4 × {17B VIN + null + 8B SecurityCode})
offset 0x132:       SKA tuples — 12 × 8 bytes:
                      status(2B) | algo(2B BE) | seed(2B BE) | key(2B BE)
```

This is exactly the data ground_truth.md decodes to.

## Why this changes the picture

The original plan was: *capture (seed, key) pairs via the shim, RE the algorithm.* But the algorithm is already RE'd. The remaining bottleneck is reduced to: **get the bench car's SSA card and look up the matching tuple for whatever seed the ECU returns.**

For the run-5/6 captured seed `0xC4DC`, three possible cases:

1. **`0xC4DC` is one of the 10–12 SKA seeds stored in the bench car's SSA card.** The matching `key` is right there in the same tuple — no algorithm needed. This is the most likely case because the seed was deterministic across two captures (which is exactly the behavior of "ECM picks the next stored SKA tuple's seed").

2. **`0xC4DC` is NOT in the bench car's stored tuples.** Then it's a fresh seed the SAS server hasn't computed for, and we'd run `(algo_from_card, 0xC4DC)` through `security_calc.py` for each algo in the card. Only one of those keys will be accepted by the ECU, and we'd find which by trying.

3. **The bench car's card has NO SKA tuples filled** (all FF). Then the SAS server hasn't paired this VIN yet — the card needs a Bojer/SAS provisioning round before unlock is possible at all.

## Falsifies Bojer's "session data" claim

We have:
- 12 ground_truth pairs all matching the static algorithm (`security_calc.py`).
- Two independent captures of the same ECU returning the same seed `0xC4DC`.

Both rule out per-session randomness or session-internal state in the algorithm. The transform is deterministic in `(algo, seed)` only. Bojer's strong-form claim is false.

## Remaining unknown

We still don't know exactly which SKA-tuple algo Tech2's `$27 $0B` flow uses for the bench car's engine ECM. That's stored in the card. **One ADB pull from the bench car's Android pairing is the last piece.**

## Tooling added

`shim/cstech2win/scripts/decode_ssa_for_seed.py` — takes a 714B SSA file (and an optional `--seed 0xXXXX`) and prints the 12 SKA tuples, then either reports the stored key for a matching seed or computes candidate keys via `security_calc.py` for every algo in the card.

Self-test against `bojer_ssa.bin`:
```
$ python3 scripts/decode_ssa_for_seed.py bojer_ssa.bin --seed 0x3949
HWKID:       Q000000010
Version:     0x12EF (4847)
SKA tuples:
  #00 @ 0x132  status=0x0000  algo=0x0366  seed=0x3949  key=0x8249
  #01 @ 0x13A  status=0x0000  algo=0x0361  seed=0xDA34  key=0x4100
  ...
Looking up seed 0x3949...
  ✓ FOUND in tuple #00: algo=0x0366, key=0x8249
    (no algorithm computation needed — key is stored in card)
```

## Next step

```
adb pull /sdcard/Android/data/com.example.saab_security_access/files/captures/<latest>.bin /tmp/bench.bin
python3 shim/cstech2win/scripts/decode_ssa_for_seed.py /tmp/bench.bin --seed 0xC4DC
```

If a tuple matches: that's the key, send it via `$27 $0C XX YY`. If no tuple matches: pair via Bojer first to populate the card, then re-pull.
