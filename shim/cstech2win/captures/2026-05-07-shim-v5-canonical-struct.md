# 2026-05-07 — run 5 with canonical struct fix → 🎯 first seed captured

**Shim build:** commit `eb9022c` (canonical PDU_EVENT_ITEM/PDU_RESULT_DATA struct from JohnJocke's `pdu_api.h`, callback trampoline disabled to stop signature-mismatch crashes).

**Raw log:** [`2026-05-07-shim-v5-canonical-struct.log`](2026-05-07-shim-v5-canonical-struct.log) (1725 lines, 168 KB).

## Headline result

**First captured `$27 $0B` seed: `0xC4DC`** for engine ECM `$0241`.

```
t=39262 ms  REQ-PDU  | len=6 | 00 00 02 41 27 0B
t=39411 ms  RSP-UDS  | len=7 | 00 00 06 41 7F 27 78         ← negative: $78 ResponsePending (~150 ms compute)
t=39576 ms  RSP-UDS  | len=8 | 00 00 06 41 67 0B C4 DC      ← positive: SEED = 0xC4DC
                              └── CAN ID ──┘ └── UDS ──┘
```

Confirms three things at once:

1. **`$Level $0B` is the real SAAB SecurityAccess level for the engine ECM** — wire format matches GMW3110 §8.8.5.1 byte-for-byte (`PCI=4, $67, echo $0B, 16-bit seed BE`).
2. **The shim's struct fix (`b58f0b0`) works** — `RSP-UDS` lines decode `PDU_RESULT_DATA->pDataBytes` cleanly.
3. **Two-phase response is normal for `$0B`** — first `$78 RequestCorrectlyReceived-ResponsePending` ~150 ms after the request, then the actual seed ~165 ms after that. So `$27 $0B` reliably produces *two* RSP-UDS lines, in that order. The total request→seed latency is ~315 ms.

## What didn't happen: no `$27 $0C` sendKey

After the seed arrived at t=39576, Tech2 did NOT send a `$27 $0C` (sendKey). It went on to other reads (`AA 01 01` telemetry, `FE 3E` TesterPresents). Most likely reason: Tech2's seed→key path (sasbridge.dll → SAS server) is unreachable from this bench, so it has the seed but can't compute a key.

This means run 5 alone gives us:
- **One half of one (seed, key) pair: `seed = 0xC4DC, key = ?`**

To extract the algorithm we need either (a) Tech2 in an environment that can reach the SAS server (so `$27 $0C` actually fires), or (b) historical (seed, key) pairs from someone else who already captured complete unlocks. Per `project_saab_ssa_ground_truth_logs.md` we have desktop-side TIS2Web logs at `~/Desktop/tis2web_logs/` that may contain complete cycles — worth checking.

## Cross-reference with Bojer's "session data" claim

The captured seed is `0xC4DC` — non-zero, non-$FFFF, falls in the GMW3110-permitted range. Bojer's strongest version of the "session data" claim ("seed depends on session-internal state") would require seeds to vary even when the ECU's persistent state is unchanged. To disprove this we need the same ECU to produce the same seed across a power-cycle — that's the next experiment. If `0xC4DC` repeats on a cold start with no prior unlock attempt, the seed is deterministic per ECU and Bojer's strong-form claim is falsified.

## Other observations from the same log

- **CB | register | tramp=DISABLED** lines appear — the trampoline-disable from this commit is working: callback registrations are tracked but Tech2's real callback is passed through unmodified, no crashes.
- **`hCop` field is now decoded correctly** (`0xF3`, `0x12A`, `0x12B` etc., matching what `PDUStartComPrimitive` returned). Confirms canonical struct layout is right.
- **Other UDS responses also decode cleanly:** at t=41330 we see `RSP-UDS | len=12 | 00 00 05 41 01 78 01 01 00 FD B6 FC` — that's a UUDT response (CAN `$0541`) with periodic data. UUDT response IDs are in the `$540` range per GMW3110 §4.4.3, confirmed.

## Next steps (in priority order)

1. **Repeat the capture across cold starts** to determine seed determinism. Power off → wait 30s → power on → run Tech2 → capture. If we get `0xC4DC` again, deterministic. If we get a different seed, randomized per session.
2. **Check `~/Desktop/tis2web_logs/`** for complete `$27 $0B`/`$27 $0C` cycles from past sessions — those would give us seed/key pairs to start RE'ing the algorithm without needing to reach the SAS server live.
3. **If Tech2 can be configured to point at a local/Bojer SAS endpoint**, redo the capture so `$27 $0C` actually fires. Then we have full pairs from the bench.
4. **Static analysis of `sasbridge.dll`** if we can't get pairs any other way. The function `sasbridge!ComputeKeyForSeed` (or whatever it's called) is the algorithm; reading its disassembly is more efficient than enumerating pairs once we have a starting seed `0xC4DC` to set as a breakpoint condition.

## Q1/Q2 status

- **Q1 (where do response bytes live):** **fully resolved.** `PDU_EVENT_ITEM.pData → PDU_RESULT_DATA.pDataBytes`. Canonical struct from `pdu_api.h`. Queue path works for SecurityAccess.
- **Q2 (algorithm shape):** still pending — we have one seed but no key. Once we get even one (seed, key) pair, we can start narrowing.
- **New Q3 (seed determinism):** is `seed = f(ECU, persistent_state)` (Trionic-style, deterministic) or `seed = random(session)`? Cold-start repeat capture answers this.

## Files

```
shim/cstech2win/captures/
├── 2026-05-06-shim-v1-first-run.{md,log}
├── 2026-05-06-shim-v3-ptr-deref.{md,log}
├── 2026-05-07-shim-v4-rsp-payload.{md,log}
└── 2026-05-07-shim-v5-canonical-struct.{md,log}    ← this capture
```
