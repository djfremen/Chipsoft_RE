# Chipsoft pin-mode switcher (Win10)

The Chipsoft Pro driver reads three DWORDs from
`HKLM\SOFTWARE\CHIPSOFT\Tech2Win` to decide which CAN channel is exposed:

| Value                   | DWORD | Meaning                                 |
|-------------------------|-------|-----------------------------------------|
| `Tech2Win_DropCAN3_11`  | 1     | Drop HSCAN, keep SWCAN-on-pin-1 active  |
| `Tech2Win_DropSWCAN1`   | 1     | Drop SWCAN, keep HSCAN-on-pins-3-11     |
| `Tech2Win_UseAsyncMode` | 0/1   | Async-mode flag                         |

`DropCAN3_11` and `DropSWCAN1` are mutually exclusive. `CST2WinConfig.exe` is
the official GUI that writes these. The scripts here do the same edit
non-interactively for scripted bench work.

## SAAB Trionic 8

Engine ECM speaks SWCAN @ 33.3k on pin 1. **Use SWCAN_PIN1 mode.**

## Three ways to switch

### 1. PowerShell script (programmatic, scripted)

Run elevated:

```powershell
.\Set-ChipsoftPinMode.ps1 -Mode SWCAN_PIN1
.\Set-ChipsoftPinMode.ps1 -Mode HSCAN_3_11
.\Set-ChipsoftPinMode.ps1 -ShowOnly
```

### 2. .reg files (zero-friction, double-click + UAC prompt)

- `swcan-pin1.reg`  — SAAB Trionic 8 mode
- `hscan-3-11.reg`  — HSCAN body/cabin modules

### 3. CST2WinConfig.exe (the official GUI)

Same outcome, same registry writes. Useful as a sanity check.

## After switching

**Restart Tech2Win / your J2534 client.** The driver only reads these values
at startup. Per the manual page 3: "After changing the settings it is
necessary to re-start the program which is working with CHIPSOFT J2534 Pro
adapter."

## Where this came from

Discovered in round 3 of the static RE — UTF-16 string scan of
`CSTech2Win.dll` revealed:

- `SOFTWARE\CHIPSOFT\Tech2Win`
- `Tech2Win_DropCAN3_11`
- `Tech2Win_DropSWCAN1`
- `Tech2Win_UseAsyncMode`

Plus matching radio-button captions ("Drop CAN on pins 3-11", "Drop Single
Wire CAN on pin 1") in `CST2WinConfig.exe`'s `.rsrc` resources, confirming
the GUI just writes the same DWORDs.

See `notes/2026-05-05-ghidra-transport.md` (in the repo root) for the full
discovery context.

## Notes

- Affects the **Tech2Win / J2534-mode host** flow (read by `CSTech2Win.dll`).
- Does NOT apply to the runtime J2534-2 path. There, pin alignment is set
  per channel via `PassThruIoctl(channel, SET_CONFIG, J1962_PINS = ...)`. No
  registry involvement.
- Does NOT apply to CANHacker mode (different firmware, different driver,
  no `CSTech2Win.dll` involvement).
