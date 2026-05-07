# Feature request — live SAS exchange monitor

**Status:** proposed, not yet implemented.
**Origin:** operator request 2026-05-07 during shim v6 capture sessions, after we confirmed seed determinism (`$0xC4DC` repeating across runs) and the `RSP-UDS`-via-fixed-struct decode path.
**Lives at:** future code lands in `shim/cstech2win/scripts/sas_monitor.py`. This doc is the spec.

## Why

The shim writes hundreds of pipe-delimited lines per second to `%TEMP%\cstech2win_shim_*.log` while Tech2Win runs. Every SecurityAccess event we care about — the `$27 0X` request, the `$67 0X SS SS` response, the surrounding `$1A` context reads — is buried in `EVT`/`CALL`/`RET` chatter.

Today the workflow is "run capture, copy log to chat, agent greps for `27 0[BC]` and `67 0B`". A live filter would let the operator see the same answer in real time without an agent in the loop, and would obviously surface the moment Tech2 actually sends a `$27 0C` (which it has not done in any capture so far — see [`2026-05-07-shim-v6-seed-deterministic.md`](../shim/cstech2win/captures/2026-05-07-shim-v6-seed-deterministic.md)).

## Display sketch

```
┌─ SAS Monitor ──────────────────────────────────────────┐
│ State: waiting for seed     Pairs collected: 6         │
│ Last seed: ─                Last key: ─                │
├────────────────────────────────────────────────────────┤
│ 39262ms  →  REQ  $0241  27 0B           (request seed) │
│ 39411ms  ←  NACK $0641  7F 27 78        (RCRR pending) │
│ 39576ms  ←  RSP  $0641  67 0B C4 DC     SEED: 0xC4DC ★ │
│ 39889ms  →  REQ  $0001  01 FE 3E        (TesterPresent)│
│ ...                                                    │
│                                                        │
│ Distinct pairs this session:                           │
│   $0241 / lvl 0B  seed=C4DC  key=─       seen 2×       │
│   $0241 / lvl 01  seed=F631  key=─       seen 2×       │
│   $0243 / lvl 01  seed=A0E9  key=─       seen 2×       │
└────────────────────────────────────────────────────────┘
```

State header progresses: `idle → waiting for seed → got seed (0xXXXX) → waiting for key → got key (0xYYYY) → unlocked`. Resets on next `$27 0X` request.

## Filter set

Lines that surface in the main pane:

- `REQ-PDU` containing `27 0[1-F]` — seed requests + key sends (any odd level = requestSeed, even = sendKey).
- `RSP-UDS` containing `67 0[1-F]` — positive SecurityAccess response (seed or sendKey ack).
- `RSP-UDS` containing `7F 27 XX` — negative SecurityAccess response. Highlight `XX = 78` differently (RCRR pending, expected) vs everything else (real failure).
- `REQ-PDU` containing `1A 3F` / `1A 90` — SSA / VIN reads. Context for the unlock.
- Optional toggle: `REQ-PDU` containing `AA 01 01` — Tech2 packet-poll. Useful to see "Tech2 is stuck waiting" but noisy enough that it should be off by default.

Lines that update header state but don't print:

- `EVT` rows just after `27 0[1-F]` to track CoP completion.
- `RSP-RxFlag` lines (we already print the matching `RSP-UDS`; flag is redundant for the operator view).

## Implementation

**Form:** single-file Python script, `shim/cstech2win/scripts/sas_monitor.py`. Cross-platform stdlib + `rich` (graceful fallback to plain ANSI if `rich` not installed). ~100–150 lines.

**Source of truth:** tail the file at `%TEMP%\cstech2win_shim_*.log`, picking the newest by mtime at startup. Watch the parent dir for new files via polling (1 Hz is fine — Tech2 restarts are seconds-scale events) and switch to a fresher file when one appears, without losing state.

Why file-tail and not a live socket: the shim already flushes per-line and writes to `%TEMP%` reliably. Adding a named pipe / UDP sink to the shim is a larger change with more failure modes (missed events on monitor disconnect, ordering with file log, etc.). File-tail is good enough until we have a concrete use case for sub-frame latency or off-host monitoring.

**State model:**

```python
@dataclass
class SasPair:
    target: int          # CAN ID, e.g. 0x0241
    level: int           # 0x01, 0x0B, ...
    seed: Optional[int]  # 16-bit
    key: Optional[int]   # 16-bit
    seen: int = 1
```

Keyed in a dict by `(target, level)`. New pair created on `$27 0X` request, seed filled in on matching `$67 0X SS SS`, key filled in when we see Tech2 send `$27 (X+1) KK KK`. Repeated identical seeds bump `seen`.

On `Ctrl-C` exit: dump the dict as CSV (`target_canid,level,seed_hex,key_hex,seen_count`) into the working directory. Useful for sharing with the algorithm-side tooling (`security_calc.py` / `decode_ssa_for_seed.py`).

## Acceptance

1. Run the monitor in one terminal, run a fresh Tech2Win SecurityAccess attempt with the v6 shim deployed. Within a second of the `$27 0B` request, the SEED line appears in the monitor with `0xC4DC` highlighted.
2. Run the same capture again. The pairs panel shows `$0241 / lvl 0B seed=C4DC seen 2×`. No duplicate event spam in the main pane.
3. Operator can `Ctrl-C` and find a CSV with all `(target, level, seed, key)` tuples seen — including the seven-ish `$01` SPS pairs Tech2 always enumerates first.

## Out of scope for v1

- **Web UI** — same core logic streamed via SSE to a browser tab. Useful for sharing screenshots / showing somebody else over a screen share. Easy follow-on, but Python-terminal is enough for the operator-at-the-laptop case.
- **Live event sink in the shim** — named pipe or UDP. Replaces file-tail. Sub-millisecond latency, supports remote monitor. Unnecessary today.
- **Decoding into "candidate keys"** in real time — calling `security_calc.py` against the seed and showing the candidate `key = f(algo, seed)` for every algo in the loaded SSA card. Cool, but it's a separate tool that already exists and operates on captured data, not live data. Save for later if it ever becomes useful.

## Notes for whoever builds this

- The shim's pipe-delimited format is: `ms_since_attach | tid | tag | function | detail`. The `detail` field for HEX rows looks like `len=N|XX XX XX ...`. Parse defensively — early lines have a different shape (`# log file: ...`, `INIT |...`).
- The CAN ID in `REQ-PDU` and `RSP-UDS` lines is the first 4 bytes of the `len=N|...` payload, big-endian. So `00 00 02 41` → `$0241`.
- `RSP-UDS` length includes the 4-byte CAN ID prefix. Real UDS payload is bytes 4..len-1.
- Don't try to parse the `EVT-RAW` / `RSP-RxFlag` lines for state — they're shim-internal debugging. Stick to `REQ-PDU` and `RSP-UDS`.
- Tech2 enumerates `$27 0X` against many ECMs in a sweep before any specific one. Don't treat the first request as "the one that matters" — it's whichever the operator actually wants to track. The pairs panel showing `seen N×` solves this naturally.
