# 714B pre-auth — recipe derived from live golden + shim log

## What the 714B actually contains

Sources cross-referenced:
- Live golden: `Chipsoft_RE/shim/cstech2win/captures/2026-05-09-elitebook-pull/YS3FD49YX41012017_PRE_AUTH_READ_2026-05-09_17-20-47.bin` (714 B, real ECM read of bench)
- Shim log: `Chipsoft_RE/shim/cstech2win/captures/raw/cstech2win_shim_20260507-015619.log` (CSTech2Win PDU trace of Tech2Win driving the bench)

The 12 SKA tuples in the bin at `0x132..0x191` are the **per-ECM seeds returned by `$27 01` across the bus**. Each 8-byte tuple is `(status:u16=0x0000, algo:u16, seed:u16, key:u16=0xFFFF)`. The seed bytes are ECM-stored. The algo bytes are host-derived from VIN via `compute_tape`.

## Tuple slot → CAN ID source (10 of 12 confirmed)

| Slot | Offset | seed | algo  | request CAN ID | reply CAN ID | shim ref |
|---|---|---|---|---|---|---|
| 0 | 0x132 | 0x3B86 | 0x0366 | `0x0257` | `0x0657` | line 47537 |
| 1 | 0x13A | 0xA78C | 0x0361 | `0x0242` | `0x0642` | line 47839 |
| 2 | 0x142 | 0xF631 | 0x0365 | `0x0241` (engine) | `0x0641` | line 48344 |
| 3 | 0x14A | 0xA0E9 | 0x0339 | `0x0243` | `0x0643` | line 48689 |
| **4** | 0x152 | 0x5897 | 0x0339 | **`0x07E0`** (OBD-II) | `0x07E8` | shim 000434 line 35705 |
| 5 | 0x15A | 0x8A29 | 0x0362 | _unknown_ | _unknown_ | not in current logs |
| 6 | 0x162 | 0xB458 | 0x0360 | _unknown_ | _unknown_ | not in current logs |
| 7 | 0x16A | 0x0463 | 0x030B | `0x0246` | `0x0646` | line 48985 |
| 8 | 0x172 | 0xC86E | 0x0339 | `0x0248` | `0x0648` | line 49283 |
| 9 | 0x17A | 0x8D07 | 0x0339 | `0x024A` | `0x064A` | line 49567 |
| 10 | 0x182 | 0x8054 | 0x0339 | `0x024B` | `0x064B` | line 49856 |
| 11 | 0x18A | 0xD2DC | 0x032F | `0x07E1` (OBD-II) | `0x07E9` | line 50152 |

Two slots use **OBD-II broadcast addressing** (`0x07E0/$07E1`), the other ten use **SAAB GMW3110 physical** (`0x024N`).

## Synthesis vs live read

- `imposter/build_pre_auth.py` predicts the **algo** column correctly (via VIN-derived `compute_tape`).
- It generates **random seeds**. Live seeds are ECM-stored.
- Therefore synthesized pre-auth ≠ live pre-auth on the seed fields. Whether Bojer's post-auth (computed from synthesized seeds) is accepted by the ECM on write-back is the open question — depends on whether the ECM cryptographically validates `(seed, key)` against its stored value before accepting the SSA write.

## What Android needs to do for a live pre-auth read

```
For each (slot, can_id) in the table above:
    send $27 01 to can_id
    wait for $67 01 SS SS on can_id|0x400
    buf[SKA_BASE + slot*8 + 0..1] = 0x00 0x00         ; status
    buf[SKA_BASE + slot*8 + 2..3] = algo               ; from VIN tape
    buf[SKA_BASE + slot*8 + 4..5] = SS SS              ; collected
    buf[SKA_BASE + slot*8 + 6..7] = 0xFF 0xFF          ; key blank
Header bytes: B1 FF*11 00 01 00 00 00 FF*3 VIN(17) ...
```

12 round-trip exchanges. With raw CAN at 500k they should each take ~100ms → ~1.5s total for the full pre-auth read.

## Blocker

Android `$27 01` to `0x0241` over raw CAN currently goes silent (2026-05-11 captures `chipsoft_11-00-10.log`). Tech2Win on the same bench reaches the same ECMs at the same addresses via CSTech2Win.dll. Two probable causes to test:

1. **Protocol mode**: switch from `J2534Protocol.CAN` (raw CAN) to `J2534Protocol.ISO15765` (ISO-TP) — that protocol auto-handles non-OBD physical addressing and the chipsoft applies appropriate acceptance filters.
2. **Acceptance filter**: even with promiscuous PassFilter, the chipsoft may default-block non-OBD reply IDs. Adding an explicit allow filter for `0x0641..0x065C` might unblock.

## Slot 5 + 6 — open

CAN IDs for seeds `0x8A29` and `0xB458` are not in any existing shim log. Either (a) they were probed in a scan session we didn't capture, or (b) they come from another addressing mode. Recover by: USBPcap on the EliteBook running a full bench pre-auth, or by sweeping unknown SAAB-physical IDs (`0x244, 0x245, 0x247, 0x249, 0x24C..0x256`).
