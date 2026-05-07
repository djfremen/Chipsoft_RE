# 2026-05-06 — first shim run, SAAB SecurityAccess captured

**Shim version:** Phase 1 — commit `a31ff4f`. Cross-compiled `CSTech2Win.dll` (111 KB, x86, 29 D-PDU exports).

**Setup on Win10:** shim dropped into `C:\Program Files (x86)\CHIPSOFT_J2534_Pro_Driver\` with the original DLL renamed to `CSTech2Win_real.dll`. Tech2Win launched, vehicle connected, a SecurityAccess attempt run.

**Raw log:** [`2026-05-06-shim-v1-first-run.log`](2026-05-06-shim-v1-first-run.log) (1530 lines, 145 KB).

## Headline finding

Tech2Win sends **`$27 $0B`** to the engine ECM (`CAN $0241`) — log line 1390, `t=53422 ms`:

```
HEX | REQ-PDU | len=6 | 00 00 02 41 27 0B
                       └──CAN──┘ └─UDS─┘
                       $0241    $27 $0B
```

Per [GMW3110 §8.8.2.1](../../../wiki/sources/gmw3110-2010-quick-ref.md#level-numbering-§8821-p127), `$0B` is in the **vehicle-manufacturer-specific range (`$0B–$FA`)** — distinct from `$01/$02` (SPS programming, what Trionic.NET solves) and `$03/$04` (DevCtrl).

**This is the SAAB-specific SecurityAccess level used by the SAS-server / IMMO-mediated path.** It's the one our Bojer-mediated Android client currently has to outsource because we don't have the seed→key transform for it. Tech2 has it (in `sasbridge.dll` / SAS server); Trionic.NET doesn't.

## All $27 invocations in this capture

11 SecurityAccess requests, two distinct levels, eleven distinct target CAN IDs:

| log line | t (ms) | CAN ID | $Level | bytes | interpretation |
|---|---|---|---|---|---|
| 1262 | 47178 | `$0257` | `$01` | `27 01` | SPS probe — ECU $57 |
| 1268 | 47478 | `$0242` | `$01` | `27 01` | SPS probe — ECU $42 (transmission?) |
| 1274 | 47763 | `$0241` | `$01` | `27 01` | SPS probe — ECU $41 (engine) |
| 1280 | 48123 | `$0243` | `$01` | `27 01` | SPS probe — ECU $43 |
| 1296 | 48628 | `$07E0` | `$01` | `27 01` | SPS probe — OBD-II ECU 1 |
| 1302 | 48925 | `$0246` | `$01` | `27 01` | SPS probe — ECU $46 |
| 1308 | 49240 | `$0248` | `$01` | `27 01` | SPS probe — ECU $48 |
| 1314 | 49538 | `$024A` | `$01` | `27 01` | SPS probe — ECU $4A |
| 1320 | 49823 | `$024B` | `$01` | `27 01` | SPS probe — ECU $4B |
| 1326 | 50112 | `$07E1` | `$01` | `27 01` | SPS probe — OBD-II ECU 2 |
| **1390** | **53422** | **`$0241`** | **`$0B`** | **`27 0B`** | **SAAB-specific Security Access on engine ECM** |

The pattern is a two-phase flow:

1. **Phase A — SPS enumeration sweep (t=47.2s → 50.1s).** Tech2 sends `$27 $01` to a parade of CAN IDs in the engine/transmission/body diagnostic address space, then to the OBD-II reserved IDs. Likely probing which ECUs respond to the standard SPS-style SecurityAccess and which reject with `$7F $27 $11` (ServiceNotSupported) or stay silent. Per GMW3110 Appendix D, ECU addresses `$10–$17` are engine, `$18–$1F` transmission, `$40–$C7` body. CAN ID lower-byte = ECU node offset, so `$0241` ↔ engine, `$0257` ↔ ECU `$57`, etc. (Notably no `$24X` for `X ∈ {4,7,9,C,D,E}` in the sweep — Tech2 already knows these aren't present from prior enumeration on this VIN.)

2. **Phase B — targeted SAS request (t=53.4s).** After ~3 seconds of intervening service traffic (`$3E` TesterPresent functional broadcasts, several `$1A` Read-Data-By-Identifier with DIDs `$9A`, `$3F`, `$90`), Tech2 issues the *real* challenge: `$27 $0B` to the engine ECM. Only one such request in the entire 145 KB log. This is the unlock attempt.

## Other services observed

For context, the same log shows Tech2 exercising:

- `$3E` TesterPresent (functional, AllNode `$0101` with extended-address `$FE`) — keeping nodes from re-locking per `P3C` timeout.
- `$1A` ReadDataByIdentifier — DIDs `$9A`, `$3F`, `$90` against multiple ECUs.
- `$AA` ReadDataByPacketIdentifier — sub `$01` ID `$01` against `$0241` (engine).
- `$AE` DeviceControl — `AE 00` against `$0241`.

Routine diagnostic chatter, not security-relevant. Useful as a sanity check that the shim is faithfully forwarding the entire D-PDU API surface.

## What's missing

**No `RSP-PDU` lines.** The shim's response decoder gated on `EventType == 0x0010` (the standard ISO 22900-2 `PDU_EVT_RESULT`), but Chipsoft's CSTech2Win actually emits result items with `ItemType = 0x1300` (PDU_IT_RESULT) and `EventType = 0xF3`. The result events arrived for every request — for the `$27 $0B` we see them at log lines 53584 and 53746 (78–322 ms after the request) — but the byte payload was never dumped because the gate fired on the wrong field.

**Fixed in commit [`3eaa620`](https://github.com/djfremen/Chipsoft_RE/commit/3eaa620).** The next capture should include `RSP-PDU` lines with the actual seed bytes for `$27 $0B`. Once we have a seed, the next phase is reverse-engineering the `$0B` seed→key algorithm out of `sasbridge.dll`.

## Observations relevant to next phases

- **`PDUStartComPrimitive` `CoPType=0x8004`** — every request used this opcode. Worth checking: is `0x8004` the SAAB-specific extension or one of the standard `T_PDU_COPT` values? Need to cross-reference.
- **Two `ItemType=0x1301` events per request** (`EventType=hCoP_value`, `hCop=0`) — these look like start/queued confirmations, not results. They consistently arrive in a pair within ~1 ms of the `RET PDUStartComPrimitive`. Phase 2 logger should distinguish these from result items.
- **`PDUIoCtl` cmd `0x000C0000`, `0x000C0001`, `0x000C0002`** — three IOCTL commands fired in init. Commands in the `0x000Cxxxx` range may be SAAB-specific filter / bitrate config. Phase 2 should log the input/output buffers for these.
- **Two `hCLL` values used:** `0x00000001` (most traffic, likely the SAAB-bus link) and `0x00000005` (used for OBD-II `$07E0/$07E1`, likely a separate logical link for the EOBD subnet). Tech2 maintains them in parallel.

## Files in this capture

```
shim/cstech2win/captures/
├── 2026-05-06-shim-v1-first-run.md     ← this file
└── 2026-05-06-shim-v1-first-run.log    ← raw shim output (1530 lines, 145 KB)
```

## Next run

After updating the shim DLL on the Win10 box (pull `Chipsoft_RE` `main`, copy `build/CSTech2Win.dll` over the previous one), repeat the same SecurityAccess attempt. Expected new content in the log:

```
... CALL  PDUStartComPrimitive ... CoPType=0x8004 size=6
... HEX   REQ-PDU len=6 | 00 00 02 41 27 0B
... RET   PDUStartComPrimitive err=0 hCoP=0x0000012D
... EVT   PDUGetEventItem ... ItemType=0x1300 EventType=0xF3 ...
... HEX   RSP-PDU len=N | 00 00 06 41 67 0B SS SS  ← the seed for $27 $0B
```

Where `06 41` (CAN ID `$0641` = engine ECM USDT response) + `67 0B` (positive `$27` response, level `$0B`) + `SS SS` (16-bit seed) is what we expect per GMW3110 §8.8.5.1.

If we get a *negative* response instead — `7F 27 XX` — the `$XX` byte tells us why (`$11` not supported, `$22` sequence error, `$37` time-delay, etc.). Useful failure mode either way.
