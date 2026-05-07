# 2026-05-07 — run 6 — seed determinism confirmed

**Shim build:** same as run 5 (commit `eb9022c`).

**Raw log:** [`2026-05-07-shim-v6-seed-deterministic.log`](2026-05-07-shim-v6-seed-deterministic.log) (1802 lines, 173 KB).

## Headline finding

**Seed `0xC4DC` repeats.** Same engine ECM `$0241`, second independent capture, exact same wire bytes:

```
Run 5 (yesterday's commit 9d373a3):
  t=39576 ms  RSP-UDS | len=8 | 00 00 06 41 67 0B C4 DC

Run 6 (this capture):
  t=54202 ms  RSP-UDS | len=8 | 00 00 06 41 67 0B C4 DC
```

**The seed is deterministic per ECU, not per-session random.** This is the cleanest possible falsification of Bojer's "security access is based on session data" hypothesis — same input, same output, twice across separate Tech2Win launches.

## Why this matters

`$27 $0B` (SAAB SAS-mediated) has the same architecture as `$27 $01` (SPS, Trionic.NET-solved): a deterministic per-ECU seed that the algorithm transforms with persistent constants (HWKID and/or other ECU state). What changes between the two paths is just which algorithm you apply — not the structure of the challenge.

Per `project_saab_uds27_seed_determinism.md`, Trionic.NET's `$01` algorithm has been validated against 45 captured pairs over 3 years where the same seed always produced the same key. Run 6 confirms the same property holds for `$0B`: the seed didn't change, so the key (whatever it is) won't either, for this specific engine ECM.

**Implication for the algorithm shape:** `key = f(seed, ECU_constants_or_HWKID)`. There's no room in the GMW3110 16-bit seed/key space for cryptographic session state, and now we have empirical evidence the seed is stable across sessions. The function space is small enough for table-driven RE once we have a few `(HWKID, seed, key)` tuples from different ECUs.

## What we still need

- **The corresponding key for `seed=0xC4DC`** on this engine ECM. Tech2 still didn't send `$27 $0C` in run 6 — same as run 5. SAS server path is unreachable, so no key gets computed.
- **A second ECU's seed** (different car) to confirm that `seed = f(ECU_constants)` varies the way we expect.
- **Static analysis of `sasbridge.dll`** to extract the algorithm directly — now that we have a known-input seed `0xC4DC`, this is breakpoint-tractable.

## Other observation: ECU `$57` in `$37` lockout

Line 1441:
```
00 00 06 57 7F 27 37
```

CAN `$0657` (ECU `$57`) returned `$7F $27 $37` — `RequiredTimeDelayNotExpired`. ECU `$57` is in the 10-second post-bad-key lockout per GMW3110 §8.8.1. Doesn't affect our `$0B` engine path (different ECU, presumably from a previous attempt) but confirms the lockout state machine matches the spec. Useful as a sanity check.

## Q-tree status (cumulative)

- **Q1 (where do response bytes live):** ✓ resolved. `PDU_EVENT_ITEM.pData → PDU_RESULT_DATA.pDataBytes`.
- **Q2 (algorithm shape — `f(seed)` vs `f(seed, SSA)`):** still pending. Need a key.
- **Q3 (seed determinism):** ✓ **resolved deterministic.** Seed is constant per ECU across sessions.
- **Bojer's strong-form session-data claim:** ✓ falsified by Q3.

## Next step priority

The cheapest move to RE the algorithm is to capture even one (seed, key) pair. Two paths:

1. **Trawl `~/Desktop/tis2web_logs/`** (per `project_saab_ssa_ground_truth_logs.md`) for a complete Tech2 unlock cycle that already includes `$27 $0B` followed by `$27 $0C`. If anything in those logs has both halves, we're done with capture and into RE.

2. **Get Tech2's SAS-server path working live.** If sasbridge.dll can be pointed at a reachable server (Bojer's, ours, anyone's), `$27 $0C` will fire and the shim will catch the key.

Option 1 is faster if the data is there.

## Files

```
shim/cstech2win/captures/
├── 2026-05-06-shim-v1-first-run.{md,log}
├── 2026-05-06-shim-v3-ptr-deref.{md,log}
├── 2026-05-07-shim-v4-rsp-payload.{md,log}
├── 2026-05-07-shim-v5-canonical-struct.{md,log}
└── 2026-05-07-shim-v6-seed-deterministic.{md,log}    ← this capture
```
