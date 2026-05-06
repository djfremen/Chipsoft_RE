# Mining `rcode.gbl` for UDS — and what the answer actually was

Premise: with `tech2_port/` already containing 965 decompiled functions from
`tech2_card_saab_v148.000_en.bin` (a.k.a. `rcode.gbl`, the SAAB Tech2 Card
binary), can we extract the wire-level UDS sequence Tech2 sends to a
Trionic 8 ECM — answering the bench-session questions without bench?

**TL;DR: rcode.gbl is at the wrong layer.** It's a hardware-level tape
encoder, not a UDS framer. But the answer was already in the workspace,
just one directory over: `external/Trionic/TrionicCANLib/Trionic8.cs`.

## What rcode.gbl actually does

Confirmed by reading `tech2_port/unknown/FUN_00161e54_*.cpp` (the Tape
Shuffler, named in the project README):

```c
unaff_D4 = (byte *)0xfff907;     // hardware register
do {
  ...
  if (unaff_D7b == '\0')         bVar1 = 0x20;
  else if (unaff_D7b == '\x02')  bVar1 = 8;
  else if (unaff_D7b == '\x04')  bVar1 = 2;
  ...
  if (unaff_D2b == '\0') *unaff_D4 = 0xff - bVar1 & *unaff_D4;
  else                   *unaff_D4 = bVar1 |        *unaff_D4;
  ...
} while( true );
```

This is **bit-banging line-encoding patterns to a memory-mapped GPIO**
(`0xFFF907`). The `0x20 / 0x08 / 0x02` constants are bit masks for the
low-level pin-state encoding — nothing to do with UDS service IDs.

`0xFFF907` is referenced exactly once in the entire 965-function dump.
The Tape Shuffler is the only customer.

Conclusion: rcode.gbl operates **below** UDS — it's converting an already-
chosen "tape" sequence into pin-toggle patterns for the Tech2 hardware. The
UDS framing decisions live somewhere above (Tech2 hardware firmware, or
`Tech2Win.exe` scaffolding).

Cross-checks that confirm this:

- `0x27` literal hits across all 952 unknown functions: ~10 files, but
  every match I sampled was a loop counter or pointer offset (e.g.
  `iVar6 = 0x27; do { *(byte*)(iVar6 + 0x1eabdf); ... }`), not a SID.
- `0x7E0` / `0x7E8` arbitration-ID hits: every match was a struct field
  offset (`*(short *)(param_1 + 0x244)`), not a CAN ID literal.
- `0xB9` (the pre-auth read mystery): zero hits in rcode.gbl.

This is consistent with the README's note: "the high-level VM (Algorithm
execution) is likely performed by the external hardware or the PC-side
sasbridge.dll." rcode.gbl is below that VM, doing line-level signaling.

## Where the answer actually was

`saab_security_project/external/Trionic/TrionicCANLib/Trionic8.cs` —
the open-source [mattiasclaesson/Trionic](https://github.com/mattiasclaesson/Trionic)
library, already cloned in the workspace. The seed→key algorithm in this
library is what 45/45 captured pairs already validated.

`Trionic8.cs::RequestSecurityAccess()` (lines 310-419) is the SAAB
Trionic 8 SecurityAccess sequence at the wire level:

```csharp
// REQUEST SEED — level 0x01
ulong cmd = 0x0000000000012702;          // bytes (LE in the ulong): 02 27 01
CANMessage msg = new CANMessage(0x7E0, 0, 3);
msg.setData(cmd);
m_canListener.setupWaitMessage(0x7E8);
canUsbDevice.sendMessage(msg);

// RESPONSE — 04 67 01 SS SS
response = m_canListener.waitMessage(timeoutP2ct);
if (response.getCanData(1) == 0x67) {
    if (response.getCanData(2) == 0x01) {
        seed[0] = response.getCanData(3);
        seed[1] = response.getCanData(4);

        // Special case: seed (00 00) means already granted
        if (seed[0] == 0 && seed[1] == 0) return true;

        // Compute key — Trionic8 + ME96 algorithms in SeedToKey.cs
        key = s2k.calculateKey(seed, _securityLevel);

        // SEND KEY — 04 27 02 KK KK
        ulong keydata = 0x0000000000022704;
        keydata ^= ((ulong)key[1] << 32);  // KK_high
        keydata ^= ((ulong)key[0] << 24);  // KK_low
        msg = new CANMessage(0x7E0, 0, 5);
        msg.setData(keydata);
        canUsbDevice.sendMessage(msg);

        // RESPONSE — 02 67 02 (granted) or 03 7F 27 ER (denied)
        response = m_canListener.waitMessage(timeoutP2ct);
        if (response.getCanData(1) == 0x67 && response.getCanData(2) == 0x02)
            return true;
    }
}
```

Plus level `0xFD` (programming) and `0xFB` (variant) paths with the same
shape, just different sublevel bytes.

## What this answers from the bench plan

| Bench-plan open question | Answer (from Trionic8.cs) |
|---|---|
| Does Tech2 send `0x10 0x03` ExtendedSession before `0x27`? | **No.** Trionic 8 SecurityAccess level 01 doesn't need extended session. The library goes straight to `0x27 0x01`. |
| TesterPresent (`0x3E 0x00`) cadence during the wait? | **Only during long waits.** Trionic8.cs calls `SendKeepAlive()` on a 1-second loop while `secondsToWait > 0`. Otherwise, no periodic TesterPresent during a normal unlock. |
| What is the pre-auth PI `0xB9` read in earlier logs? | **`GetPIB9()` in Trionic8.cs line 1736.** Comment: *"Subnet config list highspeed - ECM, ABS, SADS, TCM, CIM"*. 2-byte read enumerating which modules are present on the high-speed CAN bus. **Diagnostic / UI population, not security-related.** |
| CAN arbitration IDs | **TX `0x7E0`, RX `0x7E8`, 11-bit, ISO-TP single frames** (payloads ≤ 7 bytes). |
| ECM-side seed-zero behaviour | **Already-granted.** Seed `(00 00)` means SecurityAccess is already open; library returns success without sending the key. |

## What still needs the bench (or one more RE step)

| Question | Why bench/RE-only |
|---|---|
| ProtocolID Tech2 picks for the ECM in J2534 | Not in Trionic8.cs (it talks raw CAN through ELM327 / Kvaser, not J2534). Bench `LogLevel:0` shows it. |
| `J1962_PINS` IOCTL value | Same reason. `Tech2Win_DropCAN3_11=1` strongly implies pin-1 SW-CAN for body, but the engine ECM is on HS-CAN (pins 6/14) at 500k, so the relevant IOCTL is for the engine path specifically. Bench answers in one log line. |
| Does Tech2 do anything before `0x27` we didn't anticipate? | Bench `(W) >>` markers show the full sequence. The only known pre-auth read is `B9`, and it's now explained. |

## Net effect on the plan

- Bench session is no longer the primary source of truth for the UDS
  sequence — Trionic8.cs is. The bench answers the J2534-specific
  ProtocolID + J1962_PINS questions, and that's it.
- The Kotlin client can be written **right now** against Trionic8.cs's
  flow, with a placeholder J2534 init that gets corrected after bench.
- For an Android-direct path through ELM327 / OBDLink SX (not Chipsoft),
  there's nothing to wait for — the entire flow including SecurityAccess
  is implementable from this file alone.

## Files used

- `saab_security_project/new_decompile/projects/tech2_port/README.md` —
  rcode.gbl context (Tape Shuffler @ FUN_00161e54, register 0xFFF907)
- `saab_security_project/new_decompile/projects/tech2_port/unknown/FUN_00161e54_00161e54.cpp`
- `saab_security_project/external/Trionic/TrionicCANLib/Trionic8.cs`
  (lines 310-419 = `RequestSecurityAccess`, lines 1735-1749 = `GetPIB9`)
- `saab_security_project/external/Trionic/TrionicCANLib/SeedToKey.cs`
  (already validated 45/45)
