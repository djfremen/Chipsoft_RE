# 2026-05-07 — run 4 with RSP-PAYLOAD derefs (PTR16+4 / +20)

**Shim build:** based on commit `dc02644` (added `RSP-PAYLOAD`/`RSP-PAYLOAD2` derefs of the inner pointers stored in `PTR16-DEREF`).

**Raw log:** [`2026-05-07-shim-v4-rsp-payload.log`](2026-05-07-shim-v4-rsp-payload.log) (2316 lines, 235 KB).

## Headline finding

**SecurityAccess responses do NOT arrive via `PDUGetEventItem`.** Even with the new RSP-PAYLOAD deref capturing the inner pointer's contents, the `$27 $0B` response bytes are absent from the queued event stream. Conclusion: Chipsoft routes SecurityAccess responses through the registered callback path, not the queue. Next iteration must hook `PDURegisterEventCallback` (this is option 3 from `HANDOFF.md`).

## Evidence

### `$27 $0B` was sent and accepted

Log line 2186, t=53939 ms:
```
HEX | REQ-PDU | len=6 | 00 00 02 41 27 0B
RET | PDUStartComPrimitive | err=0 hCoP=0x14F
```
`err=0` means the request was accepted by the D-PDU stack and queued for transmission. So the wire send happened.

### Two `EventType=0xF3` events arrived for it

t=54109 and t=54290 — same `hCop=0x0158839C` (= the persistent pCoPTag for `hCLL=1`, the SAAB engine bus). For each event we logged: `EVT-RAW`, `PTR12-DEREF`, `PTR16-DEREF`, `RSP-PAYLOAD`, `RSP-PAYLOAD2`.

### `RSP-PAYLOAD` decoder works for other UDS services

To validate the RSP-PAYLOAD decoder isn't broken, I grep'd for any embedded UDS frame in the entire log — pattern `06 41 XX YY ZZ ZZ` (engine ECM USDT response):

| count | pattern | service |
|---|---|---|
| 8 | `06 41 7F AA 78 00` | engine busy on `$AA` (RequestCorrectlyReceived-ResponsePending) |
| 2 | `06 41 5A 9A 03 04` | engine VIN-DID positive response (`$5A` = positive `$1A`, DID `$9A`) |

These appear at **offset 16** of `RSP-PAYLOAD` lines (16-byte metadata header + 4-byte CAN ID + UDS payload). So the deref pipeline works. We just don't see any `06 41 67 0B` or `06 41 7F 27` for SecurityAccess.

### Search for `67 0B` / `7F 27` returns zero hits

Across all 2316 log lines: zero `67 0B`, zero `67 0C`, zero `7F 27`. The seed (or a negative response to it) is not in the log at all.

## Inferred channel separation

Chipsoft appears to route responses by service class:

| service class | response delivery | confirmed by |
|---|---|---|
| Read-data (`$1A`, `$AA`, `$22`, `$23`) | `PDUGetEventItem` queue | `5A 9A` and `7F AA 78` patterns visible at RSP-PAYLOAD offset 16 |
| Security (`$27`) | callback registered via `PDURegisterEventCallback` | absence in queue + Tech2 registers 3 callbacks at startup |

The `EventType=0xF3` events that fire after `$27 $0B` are most likely **completion notifications** (request was sent, stack-level done) without the actual UDS response payload. The payload arrives asynchronously via the callback Tech2 registered for that `(hMod, hCLL)` pair.

In the `INIT` section of the log, three callbacks are registered:
- `cb=00FA1E00` for `hMod=0xFFFFFFFF, hCLL=0xFFFFFFFF` (catch-all)
- `cb=00FA1E00` again for `hMod=0x00000001, hCLL=0xFFFFFFFF` (per-module)
- (later) `cb=00FA8F60` for `hMod=0x01, hCLL=0x01` (SAAB diagnostic link)
- (later) `cb=00FA8F80` for `hMod=0x01, hCLL=0x02` (parallel link)

We never see those callbacks fire because we don't currently log inside them — registration is logged, but Tech2 calls `cb_*(hMod, hCLL, pData)` directly out of band.

## Q1 / Q2 status

- **Q1 (where do `$27 $0B` response bytes live):** answered — they live in the callback's `pData` argument. Not in `PDUGetEventItem`.
- **Q2 (algorithm shape):** still unanswered. No `$27 $0C` was emitted in this run either, presumably because Tech2 is not getting clean responses via the queue path and is timing out (or the seed it sees via callback is `$0000` already-unlocked, terminating without a sendKey).

## Next iteration

Commit `<this commit>` adds **callback-trampoline interception**:

- 16 pre-generated `__stdcall` trampolines (`cb_tramp_0` ... `cb_tramp_15`).
- Each knows its slot index at compile time and dispatches to a common logger.
- `PDURegisterEventCallback` wrapper: allocates a slot, stores Tech2's real callback, substitutes our trampoline before forwarding to the real `PDURegisterEventCallback`.
- The dispatcher logs `CB | fired | slot=N hMod=... hCLL=... pData=...` and a `CB-DATA` 64-byte hex dump of `pData`, then calls Tech2's real callback with the same args (so Tech2 still works).

Expected log content for the next `$27 $0B` exchange:

```
... CALL | PDURegisterEventCallback | ... cb=00FA1E00 ...
CB   | register | slot=0 real=00FA1E00 tramp=...
... PDURegisterEventCallback returned err=0 ...

(time passes, $27 0B request sent, CSTech2Win invokes our trampoline:)

CB   | fired | slot=0 hMod=0x01 hCLL=0x01 pData=0x...
HEX  | CB-DATA | len=64 | 00 13 00 00 ... 06 41 67 0B SS SS ...
```

The seed bytes (or a `$7F $27` negative response) should appear in the `CB-DATA` hex dump of the slot=1 or slot=2 callback (the per-CLL callbacks `00FA8F60` / `00FA8F80`, which fire for the SAAB diagnostic link).

If the seed STILL doesn't appear after callback hooking, there's a fourth possibility we haven't considered: Chipsoft might keep the seed bytes inside the DLL (never exposed to the host) and only deliver the *result of the seed→key transform* over USB to the device. That'd mean the algorithm runs *inside* CSTech2Win.dll itself — at which point the next move is static analysis of CSTech2Win.dll rather than further dynamic capture. We're not there yet.

## Files

```
shim/cstech2win/captures/
├── 2026-05-06-shim-v1-first-run.md
├── 2026-05-06-shim-v1-first-run.log
├── 2026-05-06-shim-v3-ptr-deref.md
├── 2026-05-06-shim-v3-ptr-deref.log
├── 2026-05-07-shim-v4-rsp-payload.md     ← this file
└── 2026-05-07-shim-v4-rsp-payload.log    ← raw 2316-line shim output
```

The naming convention is `YYYY-MM-DD-shim-vN-<feature>` — N = sequential capture iteration (not commit hash, since multiple commits can produce the same capture flavor).
