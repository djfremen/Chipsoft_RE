# 2026-05-07 — bench car Bojer round-trip → 11/11 algorithm validation + 6 candidate keys

## What we did

1. Built an imposter pre-auth for the bench car's VIN `YS3FH46U681101367` via `saab-security-api/imposter/build_pre_auth.py`. The bench car is in `saab_codes.db` (security code `J2AQD3HH`).
2. Posted the 714-byte pre-auth to Bojer's `https://sas.mysaab.info/api/process` (one civil request, `User-Agent: OpenClaw imposter-differential/1.0`).
3. Bojer returned a 714-byte post-auth with HWKID stamped `S000310723`, version bumped to `0x12EF`, and 11 SKA tuples populated with keys.
4. Ran `security_calc.get_key_from_seed(seed, algo)` against all 11 returned `(algo, seed, key)` tuples.

## Result

**11/11 match.** `security_calc.py` produced the exact same key as Bojer for every tuple. Combined with the earlier 12/12 match against `~/Desktop/tis2web_logs/ground_truth.md`, we now have **23/23 total agreement** with Bojer across two independent VINs and two independent runs.

```
algo    seed    bojer_key   local_calc   result
0x0360  0xC53E  0x066D     →  0x066D     OK
0x0331  0xD755  0x24C3     →  0x24C3     OK
0x0369  0x14BA  0x06A2     →  0x06A2     OK
0x0366  0x8490  0xAF66     →  0xAF66     OK
0x0366  0xF8CB  0x8050     →  0x8050     OK
0x0366  0xCF53  0xDA73     →  0xDA73     OK
0x033C  0x9B4B  0xD667     →  0xD667     OK
0x0309  0xF404  0xE79B     →  0xE79B     OK
0x0360  0xB752  0x458E     →  0x458E     OK
0x0331  0x6FD7  0x4E4B     →  0x4E4B     OK
0x0369  0x474E  0x3851     →  0x3851     OK
```

The algorithm is `dllsecurity.dll::SetSeedAndGetKey`, RE'd in `security_calc.py`. We can stop calling Bojer for keys.

## Candidate keys for the bench car's actual seed `0xC4DC`

Per runs 5/6 of the shim, the bench car engine ECM returns `seed = 0xC4DC` deterministically when challenged with `$27 $0B`. It's not in the imposter-generated tuples, but the algo for `0xC4DC` is one of the 6 distinct algos seen in this card:

```
algo  appearances  key for seed 0xC4DC
0x0366    3×       0xB097    ← most-likely default
0x0360    2×       0xE666
0x0331    2×       0x939B
0x0369    2×       0x4617
0x033C    1×       0x453D
0x0309    1×       0x17C3
```

Try in the order shown above. Per GMW3110 §8.8.6.2, after 2 wrong keys the ECM imposes a 10-second time-delay before accepting the next `$27`. So six attempts split across three lockout cycles, ~30 seconds total worst case.

## Even better path: pull the bench car's actual SSA

If the bench car has ever been paired through the Android client, its 714 B SSA capture is at `/sdcard/Android/data/com.example.saab_security_access/files/captures/` per `reference_saab_field_capture_location.md`. That card has the exact (algo, seed, key) tuples the ECU was programmed with, including the one for seed `0xC4DC`. Run:

```
adb pull /sdcard/Android/data/com.example.saab_security_access/files/captures/<latest>.bin /tmp/bench.bin
python3 Chipsoft_RE/shim/cstech2win/scripts/decode_ssa_for_seed.py /tmp/bench.bin --seed 0xC4DC
```

If the seed is in the card → exact key, no guessing.

## Falsification status of Bojer's "session data" claim

| evidence point | status |
|---|---|
| 2 deterministic captures of `0xC4DC` | seed is `f(ECU_state)`, not random |
| 12 ground_truth pairs match local algo | algorithm is `f(algo, seed)` only |
| 11 fresh-Bojer pairs match local algo | algorithm is reproducible without Bojer |
| Bojer's response carries the same shape Tech2's Java code expects | dllsecurity.dll IS the SAS engine |

Strong-form claim ("session-internal state"): falsified.
Medium-form claim ("requires per-ECU context like HWKID"): true but doesn't block us — we have HWKIDs from pairing.
Weak-form claim ("roundtrip required per session"): trivially true, irrelevant to algorithm RE.

## Files

```
shim/cstech2win/captures/
├── ...
├── 2026-05-07-bench-car-pre-auth.bin       ← imposter input to Bojer
├── 2026-05-07-bench-car-bojer-post-auth.bin ← Bojer's response (HWKID S000310723, keys populated)
└── 2026-05-07-bench-car-bojer-roundtrip.md  ← this file
```
