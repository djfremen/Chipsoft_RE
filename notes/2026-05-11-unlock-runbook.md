# SAAB SAS unlock — end-to-end runbook (2026-05-11)

Every command, every byte, every offset for the bench 2017 engine ECM unlock.
Status today: Bojer roundtrip + key derivation are fully working on-device.
Live `$27 0B → $27 0C` write-back is gated on `$0241` raw-CAN transport (silent
in current chipsoft-android session — separate problem).

## A. The 714B SSA pre-auth → post-auth pipeline

Three steps. The 714B carries both **the unlock card** the ECM will store
back to flash AND **the engine SAS key** the host will send on the wire.

### A.1  Pre-auth read (12 ECMs over CAN)

Address each ECM with `$27 $01` (SecurityAccess seed request, level 1) and
copy the returned 2-byte seed into a fixed tuple slot of the 714B.

| Slot | Offset | Request CAN ID | Reply CAN ID | Algo (host-derived) | Source ECM |
|---|---|---|---|---|---|
| 0  | `0x132` | `0x0257` | `0x0657` | `0x0366` | (BCM/UEC) |
| 1  | `0x13A` | `0x0242` | `0x0642` | `0x0361` | trans/ABS |
| 2  | `0x142` | `0x0241` | `0x0641` | `0x0365` | **engine ECM** |
| 3  | `0x14A` | `0x0243` | `0x0643` | `0x0339` | brake |
| 4  | `0x152` | `0x07E0` | `0x07E8` | `0x0339` | OBD-II eng |
| 5  | `0x15A` | _unknown_ | _unknown_ | `0x0362` | (not in our shim logs yet) |
| 6  | `0x162` | _unknown_ | _unknown_ | `0x0360` | (not in our shim logs yet) |
| 7  | `0x16A` | `0x0246` | `0x0646` | `0x030B` | airbag |
| 8  | `0x172` | `0x0248` | `0x0648` | `0x0339` | climate |
| 9  | `0x17A` | `0x024A` | `0x064A` | `0x0339` | trans |
| 10 | `0x182` | `0x024B` | `0x064B` | `0x0339` | (aux) |
| 11 | `0x18A` | `0x07E1` | `0x07E9` | `0x032F` | OBD-II trans |

Each tuple: `[status:u16=0x0000][algo:u16][seed:u16][key:u16=0xFFFF]` (8 bytes,
big-endian).

Header bytes 0x00..0x2D stay (mostly) FF in pre-auth; only the VIN at
`0x14..0x24` and the file marker `B1` at `0x00` are set. Version word at
`0x0C..0x0D = 00 01`.

There is **also a "13th tuple" slot at `0x192..0x199`** that the engine ECM
uses for SAS unlock (level `$0B`). This slot is empty (`FF FF FF FF FF FF FF
FF`) in pre-auth — Bojer fills it.

### A.2  Bojer POST to `/api/process`

```python
import base64, json, urllib.request
pre = open('pre_auth_714b.bin','rb').read()
req = urllib.request.Request(
    "https://sas.mysaab.info/api/process",
    data=json.dumps({"SSA_DATA": base64.b64encode(pre).decode()}).encode(),
    headers={"Content-Type":"application/json"}, method="POST")
post = base64.b64decode(json.loads(urllib.request.urlopen(req, timeout=30).read())["SSA_DATA"])
```

Bojer returns the same 714B with these mutations (48 bytes):

| Offset | Change |
|---|---|
| `0x01..0x0B` | HWKID stamp `00 53 30 30 30 33 31 30 37 32 33` = `\x00S000310723` |
| `0x0C..0x0D` | Version `12 EF` |
| `0x10` | Clear to `FF` |
| `0x26..0x2D` | Security code (per VIN; bench 2017 = `XJOUQVL7`) |
| `tuple[i].key` (each populated tuple) | Computed key |
| `0x198..0x199` | **Engine SAS key (level `$0B`) = `4E ED` for bench 2017** |

**Synthesized pre-auths cannot substitute for a live read.** Bojer preserves
the seeds and computes keys from them; wrong seeds → wrong keys → ECM rejects
the unlock.

### A.3  Where the engine SAS key actually sits in the post-auth

The engine ECM uses level `$0B` SecurityAccess (SAAB-specific) for SSA write
authorisation. The key that satisfies that challenge is the `4E ED` Bojer
places at `0x198..0x199` of the 714B (when 12 tuples are populated).

**Caveat for partial pre-auth templates:** if your pre-auth has fewer tuples
(e.g. the bundled Android `pre_auth_2017.bin` has only 9 populated tuples
including the engine SAS at slot #8), Bojer places the `(C4DC, 4EED)` tuple
in that slot and there is *no separate `0x198` byte to read*. **Search by
seed value `0xC4DC`, not by offset.**

## B. The on-the-wire UDS unlock sequence (engine ECM)

Run on HS-CAN at 500 kbps. Request CAN ID `0x0241`, reply CAN ID `0x0641`.
All bytes single-frame ISO-TP except where multi-frame noted.

```
1) Enter extended diagnostic session
   TX  $0241  02 10 02              ; StartDiagnosticSession, sub=0x02
   RX  $0641  06 50 02 00 19 01 F4  ; positive response (timings echo)

2) Request seed
   TX  $0241  02 27 0B              ; SecurityAccess, level 0x0B (seed request)
   RX  $0641  04 67 0B C4 DC        ; seed = 0xC4DC (deterministic for this ECM)

3) Send key (computed from seed via SAAB algo 0x0367 / dllsecurity alt1 table)
   TX  $0241  04 27 0C 4E ED        ; SecurityAccess, level 0x0C (send key)
   RX  $0641  02 67 0C              ; positive ack — ECM unlocked
```

After step 3 the ECM is in "engineer mode" until session times out or `$10 81`
is sent. Within that window: write the 714B post-auth back via
`$3D` (WriteMemoryByAddress) to the SSA region; the ECM persists it to NVRAM.

## C. Local key derivation — `security_calc.py`

The host-side algorithm we have RE'd. Three lookup tables × 256 entries × 13
bytes/entry (= 3328 bytes per table). Each entry encodes 4 micro-ops on a
16-bit accumulator. `get_key_from_seed` picks the table by algo ID range:

- `algo & 0xFF00 == 0x0300` and certain low-byte ranges → alt1 (engine SAS)
- Other ranges → main or alt2

```python
# saab_security_project/SAABSecurityAccess/python_server/security_calc.py
from security_calc import get_key_from_seed

key = get_key_from_seed(seed=0xC4DC, algorithm_id=0x0367)
assert key == 0x4EED   # bench 2017 engine SAS, validated against Bojer 9/9
```

Verified 2026-05-11 against the live Bojer post-auth — every populated tuple
matches:

```
# 0 algo=0x0366 seed=0x3B86 Bojer=0x8B3D local=0x8B3D ✅
# 1 algo=0x0361 seed=0xA78C Bojer=0x73A8 local=0x73A8 ✅
# 2 algo=0x0365 seed=0xF631 Bojer=0xDE40 local=0xDE40 ✅
# 3 algo=0x0339 seed=0xA0E9 Bojer=0x068F local=0x068F ✅
# 4 algo=0x030B seed=0x0463 Bojer=0x9CC0 local=0x9CC0 ✅
# 5 algo=0x0339 seed=0xC86E Bojer=0x2FCB local=0x2FCB ✅
# 6 algo=0x0339 seed=0x8D07 Bojer=0xF5F0 local=0xF5F0 ✅
# 7 algo=0x0339 seed=0x8054 Bojer=0x5D8A local=0x5D8A ✅
# 8 algo=0x0367 seed=0xC4DC Bojer=0x4EED local=0x4EED ✅
```

## D. On-device equivalent — Kotlin `SecurityCalculator`

The same algorithm ported to Kotlin and bundled in the Android app:

- `crypto/SecurityCalculator.kt` — the VM that executes the 4-op sequence
- `crypto/SecurityTables.kt` — the three 3328-byte tables (main / alt1 / alt2)

Used directly inside `MainViewModel.runSasUnlockViaBojer`:

```kotlin
val localKey = SecurityCalculator.getKeyFromSeed(
    seed = capturedSeed,
    algorithmId = algoFromTuple and 0xFF,
    table = SecurityTables.getAlt1Table()
) and 0xFFFF
```

Cross-checked at runtime against Bojer's tuple keys — the chipsoft-android
log lines show `✅ Bojer 0x4EED == local 0x4EED` etc.

## E. Bojer roundtrip success path (Android, button 6)

`runSasUnlockViaBojer(vinSuffix="2017", code="XJOUQVL7")` in
`chipsoft-android/app/src/main/java/com/example/chipsoft_tech2/ui/MainViewModel.kt`.

1. Loads bundled `assets/pre_auth_<vinSuffix>.bin` (714 B)
2. Saves copy as `<VIN>_PRE_AUTH_for-bojer_<ts>.bin`
3. POSTs to `https://sas.mysaab.info/api/process` via `BojerApi.processPreAuth`
4. Saves response as `<VIN>_POST_AUTH_bojer_<ts>.bin`
5. Walks all SKA tuples, comparing Bojer-computed key to local
   `SecurityCalculator` derivation
6. Locates the tuple with `seed == 0xC4DC` and prints the unlock command
7. Writes a `NOTE:` line to the disk log with the full verdict

Output files land in `/sdcard/Android/data/com.example.chipsoft_tech2/files/captures/`.

## F. Known-good 2026-05-11 17:18 run

Pulled file: `YS3FD49YX41012017_POST_AUTH_bojer_2026-05-11_17-18-31.bin`

```
HWKID=S000310723   ver=0x12EF   sccode=XJOUQVL7
seed 0xC4DC at offset 0x176     key 0x4EED at offset 0x178
9/9 tuples cross-validated      saved 714B = real Bojer mutation
```

To complete unlock once `$0241` transport works: just send the 3 frames in
section B verbatim. The host already knows the key.
