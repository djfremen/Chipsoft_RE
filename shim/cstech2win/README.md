# CSTech2Win shim

A drop-in replacement for `CSTech2Win.dll` that logs every D-PDU API call Tech2Win makes to the Chipsoft Pro adapter, with full request/response byte capture for SecurityAccess flow analysis.

## Why this exists

Tech2Win uses the D-PDU API (ISO 22900-2) to talk to its J2534 adapter via `CSTech2Win.dll`. We need to capture the SecurityAccess `$27` request and seed/key response bytes during a real Tech2Win unlock attempt to identify which `$Level` SAAB's SAS-server-mediated path uses (per `wiki/sources/gmw3110-2010-quick-ref.md`). The previous capture options are all unviable:

- **`LogLevel:1` driver-side log** — confirmed unstable (`memory/project_chipsoft_loglevel1_mothballed.md`).
- **canscan.exe / canhacker firmware** — caused live-car bus disturbance during the 2026-05-06 incident.
- **Listen-only sniffer (Arduino MCP2515 or 2nd Chipsoft)** — works for HS-CAN but can't reach the SWCAN side where CIM/IMMO traffic lives.

The shim sits between Tech2Win and the real DLL with **zero bus contact**. It logs at the API boundary so the bytes are already de-framed (no ISO-TP reassembly to do). Captures everything regardless of which physical bus is involved.

## Architecture

```
   Tech2Win.exe
        │
        │ LoadLibrary("CSTech2Win.dll")
        ▼
   ┌──────────────────────┐         ┌──────────────────────┐
   │  CSTech2Win.dll      │         │  CSTech2Win_real.dll │
   │  (this shim)         │ ───────►│  (renamed original)  │
   │                      │   29    │                      │
   │  - 23 forwarders     │ exports │  Real Chipsoft impl. │
   │  - 6 instrumented:   │         │                      │
   │    PDUConstruct      │         └──────────────────────┘
   │    PDUDestruct       │                  │
   │    PDUIoCtl          │                  ▼
   │    PDUStartComPrim.  │           USB → Chipsoft Pro
   │    PDUGetEventItem   │
   │    PDURegisterEvtCb. │
   └──────────┬───────────┘
              │
              ▼
   %TEMP%\cstech2win_shim_<timestamp>.log
```

Forwarders are naked __stdcall trampolines that `jmp` to the real-DLL function pointer with the original stack intact — no calling-convention mismatch, no per-function arg knowledge needed. The 6 instrumented exports get full ISO 22900-2 signatures with arg + buffer hex logging.

## Building

### Cross-compile from macOS / Linux (recommended)

Requires MinGW-w64 32-bit toolchain.

```bash
brew install mingw-w64                        # macOS
# or: apt-get install mingw-w64               # Debian/Ubuntu

cd Chipsoft_RE/shim/cstech2win/
make regen                                    # regenerate stubs from real DLL
make                                          # builds build/CSTech2Win.dll
make inspect                                  # verify exports vs real DLL
```

Output: `build/CSTech2Win.dll` (32-bit PE, 29 exports matching the real DLL ordinals).

### Native MSVC build on Win10

TODO: `scripts/build_msvc.bat` for users who only have Visual Studio Build Tools. (Phase 1 deliverable above is the cross-compiled DLL — Chris pulls it pre-built.)

## Installing

**Find Tech2Win's `CSTech2Win.dll`.** Typical path:

```
C:\TIS2WEB\Tech2Win\CSTech2Win.dll
```

If unsure, search: `dir /s /b C:\CSTech2Win.dll`.

**Back it up, rename it, drop the shim:**

```cmd
cd C:\path\to\Tech2Win\
copy CSTech2Win.dll CSTech2Win.dll.original.bak
ren CSTech2Win.dll CSTech2Win_real.dll
copy <repo>\Chipsoft_RE\shim\cstech2win\build\CSTech2Win.dll .
```

**Important:** the shim looks for `CSTech2Win_real.dll` in the *same directory* as itself. Don't move them apart.

## Using

1. Launch Tech2Win normally.
2. Connect to the vehicle.
3. Drive a SecurityAccess attempt (any function that exercises `$27`).
4. Close Tech2Win cleanly.
5. Find the log: `%TEMP%\cstech2win_shim_<YYYYMMDD-HHMMSS>.log`.

### Log format

Pipe-delimited:

```
<ms_since_attach>|<tid>|<event>|<function>|<detail>
```

Events:
- `INIT` — DLL load, real DLL resolution
- `CALL` — instrumented function entry, with key args
- `RET ` — instrumented function exit, with return code
- `EVT ` — event item dequeued (response from ECU)
- `HEX ` — hex dump of a buffer (request bytes, response bytes)
- `EXIT` — DLL unload

### Reading a SecurityAccess capture

Look for `PDUStartComPrimitive` calls with `CoPType=0x8010` (PDU_COPT_SENDRECV — diagnostic request) and a `REQ-PDU` hex line whose bytes start with `27`. The byte after `27` is the `$Level` per GMW3110 §8.8.2.1.

Example (synthetic):
```
1234|01a4|CALL |PDUStartComPrimitive|hMod=0x00000001 hCLL=0x00000005 CoPType=0x8010 size=2
1234|01a4|HEX  |REQ-PDU|len=2|27 01
1234|01a4|RET  |PDUStartComPrimitive|err=0 hCoP=0x00000010
1239|01a4|EVT  |PDUGetEventItem|hMod=0x00000001 hCLL=0x00000005 ItemType=0x1 EventType=0x10 hCop=0x00000010 ts=12345
1239|01a4|HEX  |RSP-PDU|len=4|67 01 AB CD
```
→ Tech2Win sent `$27 $01` (requestSeed at `$Level $01`), ECU returned seed `$ABCD`.

If `$Level` ≠ `$01/$02`, that's the SAAB-specific path we're after.

## Files

```
shim/cstech2win/
├── README.md                 — this file
├── Makefile                  — MinGW-w64 cross-compile
├── scripts/
│   └── gen_shim.py           — reads real DLL, emits .def + forwarders
└── src/
    ├── shim.h                — common header
    ├── dllmain.c             — DllMain, real-DLL load/resolve
    ├── log.c                 — pipe-delimited timestamped log
    ├── wrappers.c            — instrumented exports (manual __stdcall)
    ├── cstech2win.def        — auto: export name table
    ├── forwarders.c          — auto: passthrough trampolines
    └── wrappers.h            — auto: typedefs + extern handles
```

## Phase 1 status (current)

- 23 of 29 exports forward verbatim via naked `jmp` trampolines.
- 6 instrumented: `PDUConstruct`, `PDUDestruct`, `PDUIoCtl`, `PDUStartComPrimitive`, `PDUGetEventItem`, `PDURegisterEventCallback`.
- `PDUStartComPrimitive` logs the request buffer (`REQ-PDU`).
- `PDUGetEventItem` decodes `PDU_RESULT_DATA` from event items and logs response bytes (`RSP-PDU`).
- Log file path: `%TEMP%\cstech2win_shim_<timestamp>.log`.

## Phase 2 (next)

- Full struct decoding in `PDUGetEventItem` (extra-info, error-info events, callback variant via `PDURegisterEventCallback`).
- `PDUSetComParam` logging — captures bitrate / timing config so we can confirm which bus Tech2Win opens.
- Log analyzer: parse pipe-delimited log → annotated transcript with GMW3110 §8.8 service tagging.

## Risks / known issues

- **Path collision.** If Tech2Win uses `LoadLibraryEx(LOAD_LIBRARY_SEARCH_SYSTEM32)` or has a hardcoded full path bypassing the install dir, our shim isn't loaded. Mitigation: verify with Process Monitor (`procmon.exe`) — filter on `Tech2Win.exe` + `CSTech2Win.dll` to confirm which path is loaded.
- **Calling-convention drift.** All 29 exports assumed `__stdcall`. If the real DLL uses `__cdecl` for any (unlikely for D-PDU), the forwarder's `jmp` still works but the calling code's stack expectation might break. Symptom: process crashes a few calls in. Mitigation: check the real DLL's exports with a disassembler.
- **ISO 22900-2 struct layouts.** `PDU_EVENT_ITEM` and `PDU_RESULT_DATA` minimal layouts in `wrappers.c` are based on the standard. If Chipsoft's implementation has padding differences, the response decode could read garbage or crash. Mitigation: gate the decode behind size sanity checks (already in place: max 4096 bytes).
