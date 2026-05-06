# Bench-capture plan — Tech2Win SecurityAccess on a SAAB Trionic 8 ECM

Reference algorithm: [mattiasclaesson/Trionic](https://github.com/mattiasclaesson/Trionic)
on GitHub provides the public Trionic 8 SecurityAccess seed→key implementation
(`TrionicCANLib/SeedToKey.cs`). The bench capture below verifies that public algorithm
matches Tech2's actual key for a known seed.

Goal: produce a (seed, key) pair from a known-good Tech2Win unlock, plus ground-truth
trace of the UDS sequence and (if hardware allows) the literal CAN frames on the wire.
Outputs feed two open items:

1. Verify `mattiasclaesson/Trionic — TrionicCANLib/SeedToKey.cs::calculateKey(seed, AccessLevel01)`
   produces the same key Tech2 produced. → confirms algorithm port to Kotlin is safe.
2. Confirm whether Chipsoft Pro in **CANHacker mode** sees SWCAN @ 33.3k on pin 1
   (the open question from the static RE).

## Hardware needed

- SAAB Trionic 8 ECM on the bench
- 12V bench supply (or battery) for the ECM
- "OBD SX" bench harness (passive — exposes ECM connector to a standard OBD-II port)
- OBD-II Y-splitter (3-way: ECM → tester branch + sniffer branch)
- Chipsoft J2534 Pro adapter — at least one. Two is cleaner (see below).
- Windows 10 laptop(s) with Tech2Win installed

## Two viable setups

### Setup A — TWO Chipsofts (cleanest, what Chris proposed)

```
ECM (bench, 12V) ──── OBD SX ──── OBD-II Y-splitter ──┬── [Chipsoft #1, J2534 mode, Win10 laptop #1]
                                                       │       └── Tech2Win drives the unlock
                                                       │
                                                       └── [Chipsoft #2, CANHacker mode, Win10 laptop #2]
                                                               └── lawicel sniffer, listen-only
```

Captures:
- Laptop #1: J2534 trace via `LogLevel:1` in `C:\ProgramData\CHIPSOFT_J2534\options.json`
- Laptop #2: raw CAN frames with arbitration IDs, ISO-TP framing, exact bus timing

This setup also answers "does CANHacker mode expose SWCAN on pin 1?" as a side effect.

### Setup B — ONE Chipsoft (works today with just gear on hand)

```
ECM (bench, 12V) ──── OBD SX ──── OBD-II ──── [Chipsoft, J2534 mode, Win10 laptop]
                                                  └── Tech2Win drives the unlock
                                                  └── J2534 driver logs trace to disk
```

No sniffer branch. We get:
- ✅ UDS bytes (PassThru* call payloads) → enough to verify SeedToKey.cs
- ❌ Literal CAN frames / arbitration IDs / ISO-TP segmentation behavior
- ❌ Answer to "does CANHacker mode see SWCAN on pin 1?" (defer until later)

This is enough to unblock algorithm verification + Android client work. The literal-CAN
capture is a bonus we can do later when Chris's friend's Kvaser is available, or with a
second Chipsoft.

## Prerequisites — Chipsoft setup (both setups)

1. Install Chipsoft drivers on the Win10 laptop(s). Verify in Device Manager:
   - J2534 mode → "STMicroelectronics Virtual COM Port (COMx)"
   - CANHacker mode → "CAN Hacker (COMx)"
2. Set Tech2Win config: run `CST2WinConfig.exe` → select **"Drop CAN on pins 3-11"**.
   This makes SWCAN-on-pin-1 active (SAAB Trionic 8 mode).
   Stored in registry: `HKLM\SOFTWARE\CHIPSOFT\Tech2Win\Tech2Win_DropCAN3_11 = 1`.
3. Edit `C:\ProgramData\CHIPSOFT_J2534\options.json`:
   ```json
   {
     "LogLevel": 1,
     "Pro": { "OpenPort2Mode": true, "RemapAUXToPIN": 12 }
   }
   ```
   (`LogLevel: 1` enables J2534 driver logging. Default `10` = off.)
4. Confirm Tech2Win sees the device in its adapter chooser dialog.

## Prerequisites — CANHacker laptop (Setup A only)

1. Flash device #2 to CANHacker mode via Start → Programs → CHIPSOFT J2534 Pro → "Make CANHacker"
2. Install `canhacker_driver.inf` (Win10 will require disabling driver-signature enforcement)
3. Open the CAN Hacker COM port via PuTTY/Tera Term/python:
   - Bit rate: divisor `30` (1000000 / 30 = 33333.3) — try `s30\r` or the User Def `Baudrate Reg.` setting in the CANHacker GUI
   - Open in **listen-only**: `L\r` (NOT `O\r` — listen-only never transmits, including ACKs)
   - Receive frames as: `t<id-3hex><len><data>\r` for 11-bit, `T<id-8hex><len><data>\r` for 29-bit

⚠️ **Critical**: listen-only mode. If the second adapter is in active mode, it ACKs every frame
on the bus and Tech2's transactions may behave differently than they would on a real car bus
(the ECM is the only other node on a bench rig).

## Procedure

1. Power on bench ECM (12V, GND, ignition pin if needed for the SAAB harness).
2. Verify Tech2Win connects and reads basic info from the ECM (no SecurityAccess yet — confirms bus is alive).
3. (Setup A) Start the CANHacker capture on laptop #2 — log every received line to a file with timestamp.
4. In Tech2Win, navigate to a service that requires SecurityAccess. Good candidates:
   - "Module → Engine → Programming" path
   - "Configuration / Programming" → any flash-related submenu
   - "Reset Adaptations" if it triggers auth
5. Tech2Win will prompt or proceed; the ECM will respond with `0x67 0x01 SS SS` (seed); Tech2 computes the key and sends `0x27 0x02 KK KK`; ECM responds `0x67 0x02` (granted) or `0x7F 0x27 ER` (denied).
6. Stop captures.

## What to extract from the captures

### From J2534 log (both setups)

Look for sequential `PassThruWriteMsgs` / `PassThruReadMsgs` calls. The bytes inside are
the UDS payload. Pattern:

```
PassThruWriteMsgs: [00 00 07 E0 02 27 01]                     ← request seed (level 0x01)
PassThruReadMsgs:  [00 00 07 E8 04 67 01 SS SS]               ← seed = SS SS
PassThruWriteMsgs: [00 00 07 E0 04 27 02 KK KK]               ← send key
PassThruReadMsgs:  [00 00 07 E8 02 67 02]                     ← granted
```

Save as: `notes/captures/2026-MM-DD-tech2win-securityaccess.j2534-trace.log`

### From CANHacker log (Setup A only)

Same sequence at the CAN frame layer. Trionic 8 uses 11-bit IDs `0x7E0` (request) / `0x7E8`
(response) per `mattiasclaesson/Trionic — TrionicCANLib/Trionic8.cs:322-324`. ISO-TP single frames for
both directions (payloads ≤ 7 bytes fit in one frame).

```
t7E0 8 02 27 01 00 00 00 00 00      ← request seed
t7E8 8 04 67 01 SS SS 00 00 00      ← seed
t7E0 8 04 27 02 KK KK 00 00 00      ← send key
t7E8 8 02 67 02 00 00 00 00 00      ← granted
```

Save as: `notes/captures/2026-MM-DD-tech2win-securityaccess.canhacker.slcan.log`

## Verification step

Once captures are in hand, run:

```
mattiasclaesson/Trionic — TrionicCANLib/SeedToKey.cs::calculateKey(seedBytes, AccessLevel.AccessLevel01)
  → expected: produces KK KK matching the captured key
```

If equal: algorithm port to Kotlin is safe ✅
If not equal: we have a (seed, key) fixture to debug against

## Open questions this answers

- ✅ Algorithm correctness (port-ready)
- ✅ Tech2's exact UDS sequence (does it send `0x10 0x03` first? TesterPresent cycling?)
- ✅ (Setup A only) CAN-layer details: arbitration IDs, ISO-TP segmentation, timing
- ✅ (Setup A only) Whether CANHacker mode exposes SWCAN on pin 1

## Risks / things that might trip us up

1. **Tech2Win not provoking SecurityAccess**: simply connecting to an ECM doesn't usually
   trigger `0x27`. Tech2 only requests it when starting an operation that needs it (programming,
   adaptations reset, etc.). If captures are silent on `0x27`, try a different Tech2 menu path.
2. **Bench ECM might not be in the right state to accept SecurityAccess**: some Trionic 8 ECMs
   require the ignition signal asserted, or specific sequencing. The SAAB community wiki has
   bench wiring; consult before powering up.
3. **ACK collisions**: if Setup A and the second adapter is in active mode, Tech2 will see
   double-ACKs and behavior may differ from a real car. Always **listen-only** on the sniffer.
4. **Driver-signature on Win10**: CANHacker driver is unsigned. Need test mode or signature
   enforcement disabled.
5. **Splitter capacitance on SWCAN**: SWCAN is sensitive to bus capacitance. A long Y-splitter
   cable might degrade signal quality at 33.3k. Use short splitter, ideally < 30 cm to each branch.

## Pickup state for next session

- Files to create: `Chipsoft_RE/notes/captures/` directory
- Tools to write later: small Python script to parse Chipsoft J2534 log → extract UDS exchanges
- Code to write later: Kotlin port of `SeedToKey.cs` for Trionic 8

## Decision needed from Chris before next session

- **One Chipsoft or two?** Determines Setup A vs Setup B.
- **When?** Bench session needs ECM-on-bench setup time + Win10 laptop time. Maybe schedule
  the CANHacker-mode flash as a separate prep step from the Tech2Win run.
