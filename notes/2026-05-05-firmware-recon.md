# 2026-05-05 — Firmware reconnaissance (canhacker_pro / j2534_pro / kline_pro .bin)

## TL;DR

**The three `.bin` files are encrypted firmware blobs, not raw ARM Cortex-M images.**
Ghidra ARM decompilation is **blocked** without a device-side bootloader dump.
`binupdate.exe` is a passthrough flasher — the decryption happens in the on-device bootloader.

Pivot recommendation: drop firmware analysis for now. Move to the **opcode-mapping Ghidra script** instead.

---

## File layout

All three `.bin` files share an identical envelope:

| File | Size | First 4 bytes (LE) | Payload size |
| --- | --- | --- | --- |
| `canhacker_pro.bin` | 23,268 | `0x00005AE0` = 23,264 | 23,264 |
| `j2534_pro.bin`     | 69,876 | `0x000110F0` = 69,872 | 69,872 |
| `kline_pro.bin`     | 13,268 | `0x000033D0` = 13,264 | 13,264 |

→ **bytes [0..3] = little-endian payload-length prefix; bytes [4..end] = payload.**

This matches the `Sent file length ` log string in `binupdate.exe`:
flash protocol is `[4-byte LE length][payload]` over the same `TransportComPort` framing the
J2534 client uses (class names `16TransportComPort`, `17TransportComPortA` are exported).

## Payload entropy

| File | Payload entropy | Zero ratio | Printable ratio |
| --- | --- | --- | --- |
| canhacker_pro | 7.991 bits/byte | 0.4% | 37.0% |
| j2534_pro     | 7.997 bits/byte | 0.4% | 37.2% |
| kline_pro     | 7.984 bits/byte | 0.4% | 37.7% |

Maximum is 8 bits/byte. The payloads are statistically indistinguishable from uniform random.
**Therefore the data is encrypted (or compressed-then-encrypted), not plain code.**

For comparison, plain ARM Cortex-M flash images have entropy ~5.5–6.5, ~2–10% zero bytes,
and the first 4 bytes form an SRAM stack pointer (`0x20XXXXXX`) — none of which is true here.

## Attacks ruled out

1. **Single-byte XOR (constant key).** Best key across all three is `0x00`
   (i.e. raw is the lowest entropy already). Ruled out.
2. **Repeating-key XOR (Vigenère-style).** Index-of-coincidence at every period
   from 1 through 2,048 is essentially `1/256 = 0.00391` — uniform-random.
   No detectable keystream period. Ruled out.
3. **Known-plaintext at offset 0/4.** Different chips, different cores, different
   payload[3]/payload[7] bytes — no predictable plaintext to anchor against.

## binupdate.exe analysis

- Compiler: GCC / TDM-MinGW (GNU C++ symbols, `__gnu_cxx::stdio_filebuf` etc.).
- Author string: `(c) 2003-2015 Denis Suprunenko, chipsoft@ukr.net`, version `v.0.3`.
- Transport: standard Win32 `CreateFileA`/`ReadFile`/`WriteFile` on a COM port,
  same `TransportComPort` class used by the J2534 stack.
- Update flow (recovered from log strings):
  1. Enumerate COM ports → `Find CHIPSOFT <type> device on `
  2. `Get boot version` → `Device boot version: ...`
  3. Send 4-byte file length → `Sent file length`
  4. Stream payload → `Update process: ...`
  5. `Reboot device - Ok`
- **No crypto constants:** searched for AES s-box / inv-sbox, CRC32 table seed
  `0x77073096`, SHA-256 `H0 = 0x6a09e667`, MD5 init `0x67452301`. **None found.**
  `fc_key` / `use_fc_key` / `fc_static` strings are TDM-MinGW pthread-cleanup TLS
  slot names from the C++ runtime, not a firmware key (false positive).
- Only large high-entropy blobs are the embedded Sectigo Authenticode signing
  certificate (DER ASN.1 starting at file offset `~0x7a200`).

**Inference:** binupdate.exe streams the `.bin` bytes verbatim to the device.
The decryption key lives in the on-device bootloader, not on the host.

## What it would take to break

1. **Dump the bootloader** from a physical Chipsoft device via SWD/JTAG. Likely
   blocked by STM32 RDP (Read-Out Protection); RDP-1 means a forced unprotect
   wipes flash, RDP-2 is permanent. Realistic only with chip-level techniques
   (glitching, decapping) or a known dev-mode unlock.
2. **Side-channel from bench captures.** Run `binupdate.exe` against a real
   device while capturing USB-CDC traffic; observe whether any byte-level
   transform happens host-side before transmission. If the bytes on the wire
   match the `.bin` exactly, decryption is fully on-device (most likely case).
3. **Authenticated firmware updates aside.** Even if we extracted the key, a
   modern bootloader may also verify a signature; replacing firmware would
   require both the encryption key and a private signing key.

This is a **very high effort, very low likelihood** path without bench
hardware. Not worth pursuing for the Android-client objective.

## What this means for the Android client

- We do **not** need to understand or replace the firmware to build the
  Android client. The wire protocol (8-byte header, opcodes, checksum) is the
  client/firmware contract, and that's already mapped from `j2534_interface.dll`.
- Firmware-level questions (CAN baud-rate setup, SWCAN pin selection,
  ISO-TP framing on the bus) can be answered just as well from a live bench
  capture as from firmware decompilation.
- **Skip firmware analysis. Pivot to the opcode-mapping Ghidra script.**

## Recommended next steps (in order)

1. **Opcode-mapping Ghidra script** (~1h). Extend `tools/ghidra_scripts/`
   with a script that walks every `PassThru*_impl` and logs the opcode value
   passed to `FUN_1001d270` (the wire-write entry point per `ghidra-drain.md`).
   Closes the last static-analysis gap.
2. **Push `notes/` and `tools/` to a `djfremen/Chipsoft_RE` branch** so this
   work survives a disk failure.
3. **Schedule the bench capture session.** Setup B (one Chipsoft + ECM + OBD SX)
   answers ~80% of remaining open questions with no firmware decryption needed.
4. **Start the Kotlin USB-CDC client skeleton.** Implement the 8-byte framing
   from `ghidra-drain.md` and verify it can talk to the device. Any unknowns
   surface immediately.
