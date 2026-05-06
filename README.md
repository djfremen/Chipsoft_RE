# Chipsoft_RE — local working tree

Clone of [`djfremen/Chipsoft_RE`](https://github.com/djfremen/Chipsoft_RE). The upstream repo holds the unmodified Chipsoft J2534 Pro Driver assets; this directory adds tooling and notes.

## Layout

```
Chipsoft_RE/
├── CHIPSOFT_J2534_Pro_Driver/   # ← upstream contents (read-only mindset)
│   ├── j2534_interface.dll      # J2534 PassThru entry-point library (PE32 x86)
│   ├── CSTech2Win.dll           # D-PDU API library (PE32 x86)
│   ├── *.bin                    # Firmware: canhacker_pro / kline_pro / j2534_pro
│   ├── chipsoft_j2534_pro_*.pdf # Official manuals (EN/RU)
│   └── drivers/*.inf            # canhacker / kline driver INFs
├── android/                     # ← Android Tech2 emulator app (Compose, USB-CDC)
│   ├── app/                     #     Source + tests (UDS over CAN, seed-to-key)
│   ├── build.gradle.kts
│   └── settings.gradle.kts      #     rootProject.name = "ChipsoftTech2"
├── tools/
│   ├── pe_summary.py            # PE arch / sections / imports / exports
│   ├── disasm_export.py         # Capstone disasm of named export or RVA
│   └── ghidra_scripts/          # DumpOpcodes / DumpConfig / DumpDrain / ...
├── notes/
│   └── 2026-05-05-*.md          # Static-RE findings + opcode catalog + bench plan
└── .venv/                       # Python venv: capstone, pefile (gitignored)
```

## Android Tech2 emulator

`android/` is an Android Studio project that drives the Chipsoft J2534 Pro
adapter directly from a phone — no Windows, no PC-side Tech2Win. The first
runnable screen exercises UDS service `0x1A` (ReadEcuIdentification) against
an in-memory loopback transport so the parsing pipeline is provably working
before hardware is plugged in.

```bash
cd Chipsoft_RE/android
./gradlew :app:testDebugUnitTest    # 18 unit tests across UDS + seed-to-key
./gradlew :app:assembleDebug        # APK in app/build/outputs/apk/debug/
```

What lives there:
- `app/src/main/.../uds/` — `CanFrame`, `CanTransport` (open + send + receive),
  `Uds27Client` (SecurityAccess), `UdsReadEcuInfoClient` (ReadEcuId, single
  & first-frame ISO-TP).
- `app/src/main/.../crypto/SaabSeedToKey.kt` — Trionic 8 + ME96 seed→key
  algorithms ported from the open-source `mattiasclaesson/Trionic` library
  and validated against 45 captured ECM (seed, key) pairs from 2021-2025.
- `app/src/test/...` — JUnit 4 tests + `FakeEcuTransport` (in-memory ECM
  simulator with HappyPath / AlreadyGranted / BadKey / LockedOut / Silent
  behaviours).

The real `J2534Transport` (Chipsoft USB-CDC, 8-byte wire envelope per
`notes/2026-05-05-ghidra-drain.md`, 24 opcodes per
`notes/2026-05-05-opcode-summary.md`) is the next module to land and slots
in behind the existing `CanTransport` interface.

## Workflow

```bash
# one-time
cd Chipsoft_RE
python3 -m venv .venv
.venv/bin/pip install capstone pefile

# summarize a binary (arch, sections, imports, exports)
.venv/bin/python tools/pe_summary.py CHIPSOFT_J2534_Pro_Driver/j2534_interface.dll

# disassemble a named export (stops at first ret)
.venv/bin/python tools/disasm_export.py CHIPSOFT_J2534_Pro_Driver/j2534_interface.dll PassThruWriteMsgs

# disassemble at a raw RVA, fixed window
.venv/bin/python tools/disasm_export.py CHIPSOFT_J2534_Pro_Driver/j2534_interface.dll 0x10005680 --bytes 0x800

# list all exports
.venv/bin/python tools/disasm_export.py CHIPSOFT_J2534_Pro_Driver/j2534_interface.dll --list
```

## Why capstone (not Ghidra/IDA) as the first pass

Capstone is a *targeted* disassembler — fast, scriptable, no UI, easy to chain into automation (e.g. "diff the disassembly of all 14 exports across two driver versions"). Ghidra is the right next tool when we need a full call graph, cross-references, or a decompiler view; pefile+capstone is the right tool to enumerate, surface-map, and pull surgical excerpts.

Practical division of labor:
- **pefile** — answer "what's in this binary?" (sections, imports, exports, strings, resources)
- **capstone** — answer "what does this specific function do?" (disasm a window of bytes)
- **Ghidra** (later) — answer "show me the call graph and a C-like decompilation"

## Ghidra (headless)

JDK 21 (brew `openjdk@21`) + Ghidra 12 (brew `ghidra`). One-shot:

```bash
GHIDRA_DUMP_OUT="$PWD/notes/2026-05-05-ghidra-j2534.md" \
  ./tools/ghidra_headless.sh \
    "$PWD/ghidra_project" Chipsoft \
    -import "$PWD/CHIPSOFT_J2534_Pro_Driver/j2534_interface.dll" \
    -scriptPath "$PWD/tools/ghidra_scripts" \
    -postScript DumpJ2534Findings.java \
    -overwrite
```

The wrapper sets `JAVA_HOME` to brew's openjdk@21. Project is reusable — re-run with `-process j2534_interface.dll -noanalysis` (skip the 98s reanalysis) and a different post-script for follow-up dumps.

## Findings index

Static RE was done in 4 rounds (2026-05-05); each `notes/` file contains the
decompiles, xref maps, and a synthesis section.

| File | Round | Headline |
|---|---|---|
| `notes/2026-05-05-first-pass.md`            | capstone   | Device is USB-CDC virtual COM port; `CSTech2Win.dll` is a D-PDU API library, not a Tech2 algorithm blob |
| `notes/2026-05-05-ghidra-j2534.md`          | Ghidra 1   | Real device-I/O funcs identified — `0x10039460` opens, `0x1003dca0` writes, `0x100392f0` reads |
| `notes/2026-05-05-ghidra-deviceio.md`       | Ghidra 2   | Device opened with `CreateFileA(GENERIC_RW, FILE_FLAG_OVERLAPPED)`; **driver inherits baud from COM port** (set at USB-CDC layer) |
| `notes/2026-05-05-ghidra-transport.md`      | Ghidra 3   | Architecture is queue-based; ring buffer at `channel+0x160`; pin selection via `Tech2Win_DropCAN3_11` registry value |
| `notes/2026-05-05-ghidra-envelope.md`       | Ghidra 4a  | `FUN_1001c810` = the framer (Boost.Log strings `"(W) >> "` / `"(R) << "`) |
| `notes/2026-05-05-ghidra-drain.md`          | Ghidra 4b  | **Wire envelope solved**: 8-byte header (cmd, length, reserved, checksum) + payload, little-endian over USB-CDC |
| `notes/2026-05-05-ghidra-checksum.md`       | helper     | `FUN_100340c0` reduces to `sum(buf) & 0xFFFF` despite SIMD-style auto-vectorization |
| `notes/2026-05-05-bench-capture-plan.md`    | forward    | Plan to capture Tech2Win SecurityAccess on a SAAB Trionic 8 ECM rig for algorithm verification |
