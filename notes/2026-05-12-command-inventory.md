# CSTech2Win shim command inventory
_Generated 2026-05-12 from 5 shim logs._

## Logs ingested

| Log | Frames |
|---|---|
| `2026-05-07-shim-v6-seed-deterministic.log` | 145 |
| `2026-05-07-shim-v5-canonical-struct.log` | 129 |
| `2026-05-07-shim-v4-rsp-payload.log` | 86 |
| `2026-05-06-shim-v1-first-run.log` | 58 |
| `2026-05-06-shim-v3-ptr-deref.log` | 58 |

## Address summary

### TX addresses (Tech2 → bus)

| CAN ID | Label | Frame count |
|---|---|---|
| `$0101` | RequestToAllNodes(broadcast) | 123 |
| `$0241` | BCM/EngineDiag(SAAB) | 98 |
| `$0242` | TDM | 10 |
| `$0243` | EBCM | 10 |
| `$0246` | SIC | 10 |
| `$0248` | ECU_0x0248 | 10 |
| `$024A` | ECU_0x024A | 10 |
| `$024B` | ECU_0x024B | 10 |
| `$0257` | ECU_0x0257 | 6 |
| `$0245` | ECU_0x0245 | 5 |
| `$0249` | unknown | 5 |
| `$024F` | unknown | 5 |
| `$07E1` | OBD_ToTCM | 5 |
| `$07E0` | OBD_ToECM | 4 |
| `$0247` | SDC | 2 |

### RX addresses (bus → Tech2)

| CAN ID | Label | Frame count |
|---|---|---|
| `$0641` | MF_FromBCM(SAAB engine reply) | 26 |
| `$0541` | SF_From_0x0541 | 18 |
| `$0643` | MF_FromEBCM | 12 |
| `$0645` | MF_From_0x0645 | 10 |
| `$0647` | MF_FromSDC | 8 |
| `$0642` | MF_FromTDM | 8 |
| `$0646` | MF_FromSIC | 8 |
| `$0648` | MF_From_0x0648 | 8 |
| `$064A` | MF_From_0x064A | 8 |
| `$064B` | MF_From_0x064B | 8 |
| `$0657` | MF_From_0x0657 | 7 |
| `$07E9` | OBD_FromTCM | 6 |
| `$0649` | MF_From_0x0649 | 6 |
| `$064F` | MF_From_0x064F | 6 |
| `$07E8` | OBD_FromECM | 4 |
| `$0651` | MF_FromHVAC | 4 |
| `$065B` | MF_From_0x065B | 4 |
| `$0644` | MF_FromEHU | 4 |
| `$064D` | MF_From_0x064D | 4 |
| `$065C` | MF_From_0x065C | 4 |

## Service inventory by ECU (TX)

### `$0101` — RequestToAllNodes(broadcast)

| Service | Count | Example payloads |
|---|---|---|
| SAAB_FunctionalBroadcastPrefix | 123 | `fe 01 3e`<br>`fe 1a 9a`<br>`fe 3e` |

### `$0241` — BCM/EngineDiag(SAAB)

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByPacketIdentifier | 73 | `aa 01 01` |
| ReadDataByIdentifier | 10 | `1a 90`<br>`1a 3f` |
| SecurityAccess | 10 | `27 01`<br>`27 0b` |
| DeviceControl | 5 | `ae 00` |

### `$0242` — TDM

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifier | 5 | `1a 90` |
| SecurityAccess | 5 | `27 01` |

### `$0243` — EBCM

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifier | 5 | `1a 90` |
| SecurityAccess | 5 | `27 01` |

### `$0245` — ECU_0x0245

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifier | 5 | `1a 90` |

### `$0246` — SIC

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifier | 5 | `1a 90` |
| SecurityAccess | 5 | `27 01` |

### `$0247` — SDC

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifier | 1 | `1a 90` |
| SecurityAccess | 1 | `27 01` |

### `$0248` — ECU_0x0248

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifier | 5 | `1a 90` |
| SecurityAccess | 5 | `27 01` |

### `$0249` — unknown

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifier | 5 | `1a 90` |

### `$024A` — ECU_0x024A

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifier | 5 | `1a 90` |
| SecurityAccess | 5 | `27 01` |

### `$024B` — ECU_0x024B

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifier | 5 | `1a 90` |
| SecurityAccess | 5 | `27 01` |

### `$024F` — unknown

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifier | 5 | `1a 90` |

### `$0257` — ECU_0x0257

| Service | Count | Example payloads |
|---|---|---|
| SecurityAccess | 6 | `27 01` |

### `$07E0` — OBD_ToECM

| Service | Count | Example payloads |
|---|---|---|
| SecurityAccess | 3 | `27 01` |
| ReadDataByIdentifier | 1 | `1a 90` |

### `$07E1` — OBD_ToTCM

| Service | Count | Example payloads |
|---|---|---|
| SecurityAccess | 5 | `27 01` |

## Response inventory by ECU (RX)

### `$0541` — SF_From_0x0541

| Service | Count | Example payloads |
|---|---|---|
| SID_0x01 | 18 | `01 77 06 02 02 fd 04 fc`<br>`01 77 03 01 01 fd 04 fc`<br>`01 78 01 01 00 fd 43 fc` |

### `$0641` — MF_FromBCM(SAAB engine reply)

| Service | Count | Example payloads |
|---|---|---|
| NegativeResponse(ReadDataByPacketIdentifier, responsePending) | 8 | `7f aa 78` |
| ReadDataByIdentifierPositiveResponse | 8 | `5a 9a 03 04`<br>`5a 90 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37`<br>`5a 3f 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37` |
| SecurityAccessPositiveResponse | 4 | `67 01 f6 31`<br>`67 0b c4 dc` |
| DeviceControlPositiveResponse | 2 | `ee 00` |
| NegativeResponse(ReadDataByIdentifier, responsePending) | 2 | `7f 1a 78` |
| NegativeResponse(SecurityAccess, responsePending) | 2 | `7f 27 78` |

### `$0642` — MF_FromTDM

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 6 | `5a 9a 01 09`<br>`5a 90 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37` |
| SecurityAccessPositiveResponse | 2 | `67 01 a7 8c` |

### `$0643` — MF_FromEBCM

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 10 | `5a 9a 03 01`<br>`5a 9a 01 07`<br>`5a 90 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37` |
| SecurityAccessPositiveResponse | 2 | `67 01 a0 e9` |

### `$0644` — MF_FromEHU

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 4 | `5a 9a 01 04` |

### `$0645` — MF_From_0x0645

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 10 | `5a 9a 03 04`<br>`5a 9a 01 0a`<br>`5a 90 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37` |

### `$0646` — MF_FromSIC

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 6 | `5a 9a 01 02`<br>`5a 90 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37` |
| SecurityAccessPositiveResponse | 2 | `67 01 04 63` |

### `$0647` — MF_FromSDC

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 8 | `5a 9a 02 0a` |

### `$0648` — MF_From_0x0648

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 6 | `5a 9a 01 07`<br>`5a 90 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37` |
| SecurityAccessPositiveResponse | 2 | `67 01 c8 6e` |

### `$0649` — MF_From_0x0649

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 6 | `5a 9a 01 05`<br>`5a 90 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37` |

### `$064A` — MF_From_0x064A

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 6 | `5a 9a 01 0a`<br>`5a 90 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37` |
| SecurityAccessPositiveResponse | 2 | `67 01 8d 07` |

### `$064B` — MF_From_0x064B

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 6 | `5a 9a 01 07`<br>`5a 90 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37` |
| SecurityAccessPositiveResponse | 2 | `67 01 80 54` |

### `$064D` — MF_From_0x064D

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 4 | `5a 9a 01 04` |

### `$064F` — MF_From_0x064F

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 6 | `5a 9a 01 02`<br>`5a 90 59 53 33 46 44 34 39 59 58 34 31 30 31 32 30 31 37` |

### `$0651` — MF_FromHVAC

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 4 | `5a 9a 03 02` |

### `$0657` — MF_From_0x0657

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 4 | `5a 9a 01 05` |
| SecurityAccessPositiveResponse | 2 | `67 01 3b 86` |
| NegativeResponse(SecurityAccess, requiredTimeDelayNotExpired) | 1 | `7f 27 37` |

### `$065B` — MF_From_0x065B

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 4 | `5a 9a 03 03` |

### `$065C` — MF_From_0x065C

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 4 | `5a 9a 01 01` |

### `$07E8` — OBD_FromECM

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 4 | `5a 9a 01 06` |

### `$07E9` — OBD_FromTCM

| Service | Count | Example payloads |
|---|---|---|
| ReadDataByIdentifierPositiveResponse | 4 | `5a 9a 01 01` |
| SecurityAccessPositiveResponse | 2 | `67 01 d2 dc` |

## Negative-response code distribution

| Requested SID | NRC | Name | Count |
|---|---|---|---|
| `0x1A` (ReadDataByIdentifier) | `0x78` | responsePending | 2 |
| `0x27` (SecurityAccess) | `0x78` | responsePending | 2 |
| `0x27` (SecurityAccess) | `0x37` | requiredTimeDelayNotExpired | 1 |
| `0xAA` (ReadDataByPacketIdentifier) | `0x78` | responsePending | 8 |

## Top SIDs (TX)

| SID | Service | Count |
|---|---|---|
| `0xFE` | SAAB_FunctionalBroadcastPrefix | 123 |
| `0xAA` | ReadDataByPacketIdentifier | 73 |
| `0x1A` | ReadDataByIdentifier | 57 |
| `0x27` | SecurityAccess | 55 |
| `0xAE` | DeviceControl | 5 |

## Top SIDs (RX)

| SID | Service | Count |
|---|---|---|
| `0x5A` | ReadDataByIdentifierPositiveResponse | 110 |
| `0x67` | SecurityAccessPositiveResponse | 20 |
| `0x01` | SID_0x01 | 18 |
| `0x7F` | NegativeResponse | 13 |
| `0xEE` | DeviceControlPositiveResponse | 2 |
