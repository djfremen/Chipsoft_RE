# 2026-05-06 — run 3 with PTR12/16 derefs (and operator-added PTR40/44)

**Shim build:** based on commit `0a1ac30` (PTR12/PTR16 derefs added) + operator-added `PTR40` and `PTR44` derefs not yet committed to the repo. Both versions of the dump appear in the log.

**Raw log:** [`2026-05-06-shim-v3-ptr-deref.log`](2026-05-06-shim-v3-ptr-deref.log) (1935 lines, 205 KB).

## Headline finding

**`PTR16-DEREF` is the right pointer to follow** — but it's a `{length, pointer}` table, not the response itself. The actual UDS response bytes are one more dereference away.

For the `$27 $0B` request at log line 1786 (t=44074 ms), the next `EventType=0xF3` event (line 1790, t=44236 ms) yielded:

```
PTR16-DEREF (line 1793):
  04 00 00 00 | A0 73 54 0A | 00 00 00 00 00 00 00 00 | 04 00 00 00 | C0 73 54 0A | 00 51 A2 02 ...
  └─len=4─┘   └─ptr→data──┘  └────  reserved/zero ────┘  └─len=4─┘   └─ptr→data──┘  └─?─┘
```

Two `{length=4, pointer}` entries. **`length=4` exactly matches the expected `$27` positive response size** (`67 0B SS SS` = 4 bytes of UDS). The pointer at PTR16+4 (`0x0A5473A0`) almost certainly points to the response bytes.

This pattern is consistent across both `EventType=0xF3` events for the `$27 $0B` request (lines 1791-1799). PTR12-DEREF was inconsistent — first event yielded `5A 06 3C 00 ...` (some other buffer), second event faulted entirely. PTR16 is the reliable field for `EventType=0xF3`.

## Other observations

### `PTR40-DEREF` and `PTR44-DEREF` (operator-added, not in repo)

The operator added two more derefs at offsets 40 and 44 of the event-item buffer (from inside the second 32-byte half of the EVT-RAW dump). These derefs hit pointer-shaped values reliably for some events but fault for others — same pattern as PTR12. The information they yield duplicates what PTR16 + its inner pointer expose, so unless we see a case where PTR16's inner data is unreliable, these can be retired in the next decoder iteration.

### Tech2 did not send `$27 $0C` (sendKey) in this run

Window between `$27 $0B` (t=44074) and end of log (~50 s later):
- `01 01 FE 3E` TesterPresent functional broadcasts (multiple, expected)
- `02 41 AA 01 01` ReadDataByPacketIdentifier to engine ECM (3 instances, telemetry)
- No `27 0C`, no `1A`/`23` reads of engine ECM, nothing security-related

Two plausible reasons:
1. **Seed came back as `$0000`** — per GMW3110 §8.8.1, this signals "node already unlocked" and the tester abandons the unlock without sending a key. The ECM would have unlocked from a prior session that wasn't power-cycled.
2. **SAS server unreachable** — Tech2 got the seed but couldn't hand it to the SAS server to compute the key, so abandoned silently.

This run cannot answer **Q2** from `HANDOFF.md` (does the algorithm need SSA context). For Q2 we need a complete unlock with both `$27 $0B` and `$27 $0C` visible. Cold-start the ECM or run on a known-locked car.

### `EventType=0xF3` events fire for many requests, not just `$27`

PTR16-DEREF was non-empty for events corresponding to `AA 01 01`, `1A 9A`, etc., not just the SecurityAccess flow. This is good — the same decoder pathway will work for all UDS responses, not just `$27`. Once we have the layout fully decoded, every request/response pair will surface as `RSP-PAYLOAD` lines automatically.

## What this run answers in `HANDOFF.md` terms

- **Q1 (mechanical):** mostly answered. PTR16+4 is the seed source. Need one more capture with the just-pushed `RSP-PAYLOAD` deref to confirm the bytes literally start with `67 0B`.
- **Q2 (strategic):** unanswered. Inconclusive because no `$27 $0C` was emitted.

## Next iteration

Commit `<this commit>` adds:
- `RSP-PAYLOAD` — dereference of the pointer at PTR16+4, 32 bytes dumped.
- `RSP-PAYLOAD2` — dereference of the pointer at PTR16+20 (second `{len, ptr}` slot in the table), in case the seed lives in the second slot.

When operator runs the next capture against a **freshly powered-on, locked ECM** (so the seed is non-zero and Tech2 actually proceeds to sendKey), expected log content for the `$27 $0B` exchange:

```
HEX | REQ-PDU | len=6 | 00 00 02 41 27 0B
... PDUStartComPrimitive RET ...
EVT | PDUGetEventItem | ItemType=0x1300 EventType=0xF3 ...
HEX | EVT-RAW         | len=24 | ...
HEX | PTR12-DEREF     | len=32 | ...               ← may fault, ignore
HEX | PTR16-DEREF     | len=32 | 04 00 00 00 <ptr> ...
HEX | RSP-PAYLOAD     | len=32 | 00 00 06 41 67 0B SS SS ...   ← THE SEED IS HERE
... a few hundred ms later ...
HEX | REQ-PDU | len=8 | 00 00 02 41 27 0C KK KK     ← THE KEY (computed by Tech2)
... the $0C response with $67 $0C ack ...
```

Once we have a real `SS SS` and `KK KK` pair, we can:
1. Repeat with several different seeds to gather pairs.
2. Pass to the `saab_security_project/external/Trionic/TrionicCANLib/SeedToKey.cs`-style RE process: try the existing Trionic `$01` algorithm against the `$0B` seeds first (it's possible `$0B` shares the same transform — we don't know yet), then if that fails, pursue static analysis of `sasbridge.dll`.

## Files

```
shim/cstech2win/captures/
├── 2026-05-06-shim-v1-first-run.md
├── 2026-05-06-shim-v1-first-run.log
├── 2026-05-06-shim-v3-ptr-deref.md     ← this file
└── 2026-05-06-shim-v3-ptr-deref.log    ← raw 1935-line shim output
```

(Run 2 was the first SEH-fault iteration — captured in conversation, not as repo artifact.)
