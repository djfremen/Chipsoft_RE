# Deep static RE — opcode wrapper scan (2026-05-07)

Follow-up to the original 5-round Ghidra analysis (`2026-05-05-ghidra-*.md`). The
question for this round: **is there a hidden opcode wrapper that the original
catalog missed?** Specifically, we wanted to confirm there's no missing
"PassThruConnect-emit" or "channel-online" opcode hiding in the dispatcher.

## Method

`tools/static_re/find_opcode_wrappers.py` — capstone-based scan that:

1. Parses the PE, locates `.text` (VA `0x10001000`).
2. Disassembles the entire section with capstone x86_32.
3. Finds every `call 0x1001d270` (the `send_and_wait` dispatcher per
   `2026-05-05-ghidra-envelope.md`).
4. For each call site, walks back up to 128 bytes looking for `push <imm>`
   or `mov reg/mem, <imm>` patterns to recover the opcode constant the
   wrapper "stamps" before invoking send_and_wait.

Run: `python3 tools/static_re/find_opcode_wrappers.py [path-to-dll]`.

## Findings

26 direct call sites to `send_and_wait`. Direct-push / direct-mov-imm patterns
recover the opcode for 17 of them:

| Opcode | Catalog role | Direct-call wrapper VA |
|---|---|---|
| `0x0B` | PassThruIoctl SET_CONFIG (12B) | `0x100150E2` |
| `0x0C` | PassThruIoctl GET_CONFIG (12B) | `0x10012D62`, `0x1001588E` |
| `0x0D` | PassThruIoctl param-less query | `0x10013739` |
| `0x0E` | PassThruSetProgrammingVoltage | `0x10014951` |
| `0x0F` | PassThruWriteMsgs sync | `0x10017FBD` |
| `0x10` | PassThruReadMsgs | `0x10017256`, `0x10017656` |
| `0x11` | PassThruIoctl 4B | `0x10013A39` |
| `0x12` | PassThruIoctl 4B | `0x10013DB9` |
| `0x17` | PassThruStartMsgFilter (71B; len pushed first as 0x47) | `0x10016C61` |
| `0x18` | PassThruIoctl 4B | `0x1001408B` |
| `0x19` | PassThruStopMsgFilter | `0x1001BE92` |
| `0x1A` | PassThruStartPeriodicMsg (note: also pushes `0x19` first — chained?) | `0x1001C7D1` |
| `0x1B` | PassThruStopPeriodicMsg | `0x1001C147` |
| `0x1C` | PassThruIoctl 4B | `0x1001435B` |
| `0x20` | PassThruOpen reset / PassThruClose | `0x100104A7` |
| `0x21` | PassThruIoctl param-less query | `0x10014D99` |
| `0x22` | PassThruWriteMsgs async | `0x1001A4B7` |
| `0x23` | PassThruIoctl 8B | `0x10014653` |

Plus: opcode `0xFF` appears once at `0x100125B1` — likely a special
status/error "ack" code, not a real opcode.

## What about opcodes 0x01, 0x03, 0x05, 0x06, 0x07, 0x08?

These are in the catalog but NOT visible in this scan. Possible reasons:

1. **Indirect dispatch** — the wrapper does `mov ecx, [vtable+offset]; call ecx`
   instead of a direct `call 0x1001d270`. The original Ghidra round caught these
   via cross-referencing PassThru* exports through their `_impl` jumps.
2. **Wrappers register themselves as function pointers** in a table that
   `send_and_wait` (or its dispatcher) consults at runtime.
3. **The opcode is loaded into a register from a memory operand** the original
   round mapped — our scan only recovers `<imm>` constants.

For our Android-direct work, this doesn't hide a new opcode — it just means
those 6 catalog opcodes use a different code path. The catalog itself is
complete; the 24 documented opcodes cover the whole dispatcher.

## Implication for Android-direct unblock

Since no new opcode is hiding in `j2534_interface.dll`, the channel-online
trigger for J2534 clients **can't be a missing wire opcode**. It has to be
one of:

- **The PassThruStartMsgFilter call itself** (J2534-spec semantics: filter
  install arms the bus). Trionic.NET does PASS_FILTER + raw CAN — see the
  `chipsoft-android` repo's `Btn("PASS_FILTER promiscuous CAN — Trionic parity")`.
- **A specific magic value in one of the existing ioctls** (e.g., SET_CONFIG
  with a vendor-extended Parameter ID we haven't tried).
- **A specific call ordering** the device requires.

Empirical probing on Android-direct continues. USBPcap of TrionicCANFlasher
remains the definitive shortcut.

## Files

- `tools/static_re/find_opcode_wrappers.py` — re-runnable scan
- This note
