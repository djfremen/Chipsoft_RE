# Shim project handoff — for the next agent picking this up

You are taking over a SAAB SecurityAccess reverse-engineering effort. The shim is working; we are deep into Phase 2, with one specific question still open. Read this in full before touching code.

## What we're trying to do (one paragraph)

Tech2Win unlocks SAAB ECMs via a SecurityAccess flow whose seed→key transform lives in `sasbridge.dll` / the SAS server, not in any open-source code. The Android client we ship currently routes every unlock through Bojer's hosted service, which is the same algorithm but a remote dependency we'd like to retire. To replicate that algorithm locally we first need to capture every byte Tech2 sends and receives during a real unlock. The CSTech2Win shim is how we capture those bytes — a drop-in proxy DLL that sits between Tech2Win and Chipsoft's real `CSTech2Win.dll`, logging every D-PDU API call.

Headline finding from the 2026-05-06 capture (`captures/2026-05-06-shim-v1-first-run.md`): Tech2Win sends `$27 $0B` to the engine ECM (CAN `$0241`). Per GMW3110 §8.8.2.1 (`wiki/sources/gmw3110-2010-quick-ref.md` in the parent `saab-security-access` repo), `$0B` is in the vehicle-manufacturer-specific range — confirming this is the SAAB-specific SAS/IMMO-mediated SecurityAccess level, distinct from the standard SPS `$01/$02` level that Trionic.NET already solves. **`$27 $0B` is the level we need the seed→key transform for.**

## The open question, precisely

We have the **request** bytes (`27 0B` to CAN `$0241`) — `REQ-PDU` lines log them cleanly. We do not yet have the **response** bytes (the 16-bit seed, then later the 16-bit key). They arrive into `PDUGetEventItem` as `ItemType=0x1300 EventType=0xF3` events, but Chipsoft's `PDU_EVENT_ITEM` struct does not match the ISO 22900-2 layout — what should be a `void* pData` at offset 20 is sometimes a small int (e.g. `0x0C`, `0x1A`) and sometimes high-bit flag values like `0x80001200`. Dereferencing it always faults under SEH.

A 64-byte raw dump (run 3, `cstech2win_shim_20260506-204051.log`, available in conversation/Drive history) revealed two important things:

1. **For `EventType=0x114` events the response IS inline** in the event-item buffer at offset 32. We saw a clean `00 00 06 46 5A 90 ...VIN-17-bytes...` pattern — that's CAN `$0646` (USDT response from ECU `$46`) + UDS `$5A $90` (positive response to `$1A $90` ReadDataByIdentifier) + the VIN. Proves response data lives in the buffer for some event types.

2. **For `EventType=0xF3` events (which is what `$27 $0B` produces) the response is NOT inline** at offset 32. Layouts seen so far have metadata-shaped DWORDs there, no `67 0B` byte sequence anywhere in the 64 bytes.

So `EventType=0xF3` responses must live behind one of the pointer-shaped fields earlier in the struct. Offsets 12 and 16 both hold pointer-shaped values (`0x0275E9D0`, `0x09DAF6D0`, etc. — heap addresses on x86 Windows). The current iteration of the shim (this commit) dereferences both with SEH guards and logs `PTR12-DEREF` / `PTR16-DEREF` 32-byte hex dumps. **The next capture will tell us which (if either) contains `67 0B` for `$27 $0B` events.**

## What to look for in the next capture

After Tech2Win runs a SecurityAccess attempt, in the log find the line:

```
... HEX | REQ-PDU | len=6 | 00 00 02 41 27 0B
```

In the next ~500 ms there will be one or two `EventType=0xF3` events. Each will have:
- `EVT-RAW` — first 24 bytes of the event-item struct
- `PTR12-DEREF` — 32 bytes at the pointer stored at offset 12
- `PTR16-DEREF` — 32 bytes at the pointer stored at offset 16

**Look for `06 41 67 0B SS SS` (CAN `$0641` USDT response + UDS `$67 $0B` positive response + 16-bit seed) in either deref dump.**

Three possible outcomes:

| Outcome | What it means | Next move |
|---|---|---|
| `PTR12-DEREF` contains `67 0B` | Offset 12 is the pointer to the response buffer (or a struct that wraps it). | Refine the decoder: compute UDS-payload length from the buffer header (probably the first DWORD), extract just the relevant bytes, log as `RSP-PDU`. |
| `PTR16-DEREF` contains `67 0B` | Offset 16 is the right pointer. (Plausible — offset 16 is consistent across many events at `0x09DAF6D0`, possibly the per-CLL receive-buffer base.) | Same as above but offset 16. |
| Neither contains `67 0B` | The response arrives via callback, not via `PDUGetEventItem`. Tech2 registered three callbacks via `PDURegisterEventCallback` (`00FA1E00`, `00FA8F60`, `00FA8F80`). | Hook the callbacks: install a per-callback trampoline in `PDURegisterEventCallback` that logs args + forwards to the original. Bigger refactor but the only other place response data can be. |

A fourth possibility: the response arrives but is *encrypted/encoded* by Chipsoft before reaching the host — in which case we'd see the bytes but they wouldn't decode as `67 0B`. Unlikely, but if you see an obvious binary blob that doesn't match GMW3110 §8.8.5.1's expected layout, consider this and report.

## Repo layout (relevant parts)

```
shim/cstech2win/
├── HANDOFF.md                ← you are here
├── README.md                 ← install instructions for Tech2Win operator
├── Makefile                  ← MinGW cross-compile (BROKEN since SEH was added — MSVC only now)
├── scripts/
│   ├── gen_shim.py           ← read CSTech2Win.dll, emit .def + forwarders.c + wrappers.h
│   └── fix_msvc.py           ← post-process forwarders.c from GCC inline asm to MSVC __asm
├── src/
│   ├── shim.h                ← common header
│   ├── dllmain.c             ← DllMain, real-DLL load/resolve
│   ├── log.c                 ← pipe-delimited timestamped log
│   ├── wrappers.c            ← MANUAL instrumented exports — your edits go here
│   ├── cstech2win.def        ← auto-generated export table
│   ├── forwarders.c          ← auto-generated MSVC-syntax passthroughs
│   └── wrappers.h            ← auto-generated function-pointer typedefs
├── build/
│   └── CSTech2Win.dll        ← committed prebuilt (MSVC); replace after each rebuild
└── captures/
    ├── 2026-05-06-shim-v1-first-run.md   ← analysis of run 1 (no RSP-PDU yet, level $0B confirmed)
    └── 2026-05-06-shim-v1-first-run.log  ← raw log of run 1
```

Subsequent capture analyses go into `captures/` with `YYYY-MM-DD-shim-vN-...` naming.

## How to build

**MSVC (the working path, on Win10):**
1. `git pull` to get latest source.
2. Run `python scripts/gen_shim.py ../../CHIPSOFT_J2534_Pro_Driver/CSTech2Win.dll` — regenerates `forwarders.c`, `cstech2win.def`, `wrappers.h` from the real DLL.
3. Run `python scripts/fix_msvc.py` — converts GCC syntax in `forwarders.c` to MSVC syntax. **Note: `fix_msvc.py` currently has a hardcoded path `c:\Users\Elitebook\Desktop\can-hacker\...`. If you're not on Chris's machine, fix the path first.** A clean fix would be to make the path arg-driven or relative; pending.
4. Build with `cl /LD /Fobuild/ /Fe:build/CSTech2Win.dll src/dllmain.c src/log.c src/wrappers.c src/forwarders.c src/cstech2win.def kernel32.lib user32.lib` (or use a Visual Studio project — pick whatever's easy on the host).
5. Replace the DLL in Tech2Win's install dir (typically `C:\Program Files (x86)\CHIPSOFT_J2534_Pro_Driver\CSTech2Win.dll` — see README.md).

**MinGW cross-compile (used to work, now broken):**
Pre-SEH, `make` from macOS produced a working DLL via `i686-w64-mingw32-gcc`. The `__try`/`__except` blocks added during the Phase 2 SEH-guard work are MSVC-only — MinGW i686 doesn't support them on x86. Do NOT try to fix this by reverting SEH; the SEH is what keeps Tech2Win from crashing on bad pointers. If you need MinGW for some reason, conditionally compile the SEH (`#ifdef _MSC_VER`) — but every prod build should be MSVC-with-SEH.

## How to run a capture

Operator instructions are in `README.md`. Short version:
1. Back up Tech2Win's real `CSTech2Win.dll` to `CSTech2Win.dll.original.bak`.
2. Rename it to `CSTech2Win_real.dll`.
3. Drop the new `build/CSTech2Win.dll` in its place.
4. Launch Tech2Win, do the SecurityAccess attempt, close cleanly.
5. Log lands in `%TEMP%\cstech2win_shim_<timestamp>.log`.
6. Operator uploads to Drive, links it back to the agent.

## Background context worth knowing

- **GMW3110 §8.8 SecurityAccess spec** is in `wiki/sources/gmw3110-2010-quick-ref.md` (parent repo `saab-security-access`). Read §4 (Wire format) and §4 ($Level numbering) before touching the decoder.
- **CSTech2Win.dll vs j2534_interface.dll** — Tech2Win uses the former (D-PDU/ISO 22900-2). J2534 clients (TrionicCANFlasher) use the latter. Don't shim the wrong one. Memory: `project_chipsoft_shim_target_dll.md` in agent memory.
- **canscan.exe / canhacker firmware caused live-car bus disturbance on 2026-05-06** (BCM panic, headlights asserted to defaults, ECM went silent until adapter unplugged). Bus-level sniffing is now a *secondary* tool; the shim is the primary path because it doesn't touch the bus electrically. Memory: `project_chipsoft_loglevel1_mothballed.md` for context on why driver-side `LogLevel:1` was also dropped.
- **`$27 $01` (SPS) flow is already solved** — Trionic.NET has the algorithm, validated against 45 captured pairs over 3 years. Don't waste capture cycles re-confirming `$01`. The interesting target is `$27 $0B` (and possibly higher levels we haven't seen yet).
- **Build artifact `build/CSTech2Win.dll` is committed.** Each rebuild replaces it. Operator can `git pull` and copy without a local build environment.

## Decision tree for the next iteration

After the next capture comes back:

1. **`PTR12-DEREF` or `PTR16-DEREF` contains `67 0B`** — go straight to writing the proper decoder. Replace the layout-discovery dumps with a clean `RSP-PDU` extraction. Compute the response length from buffer metadata (probably first DWORD of the deref'd buffer, which usually is a `numBytes` field in this kind of ABI). Then drop a follow-up capture analysis into `captures/2026-05-NN-shim-vM-decoder.md` and commit the cleaned-up decoder.

2. **Neither `PTR12-DEREF` nor `PTR16-DEREF` contains `67 0B`** — pivot to callback hooking. Add a small struct that records each `(hMod, hCLL, real_cb)` registered via `PDURegisterEventCallback`, and have our wrapper substitute a logging trampoline that calls `shim_log_hex("CB-PDU", ...)` then forwards to `real_cb`. The trampoline has to match the exact `__stdcall void (UNUM32, UNUM32, void*)` signature — see existing `fn_PDURegisterEventCallback` typedef in `wrappers.c`.

3. **Both deref pointers fault** — likely means the field at offset 12 or 16 is not a pointer for `EventType=0xF3` events at all. Bump `EVT-RAW` back to 64 bytes (you'll need to check buffer validity with SEH — the original 24-byte limit was for safety) and look at offsets 24+ for inline data, or look at offsets 32+ for a possible second struct chained from the first.

In all three cases, write the analysis up under `captures/` (markdown + raw log) and commit before moving on. The `captures/2026-05-06-shim-v1-first-run.md` file is the template — keep the same structure (headline finding, table of $27 invocations, what's missing, next run).

## Working notes / quirks

- Tech2 enumerates ECUs via `$27 $01` to a parade of CAN IDs (`$241–$24F`, `$257`, `$7E0`, `$7E1`) before issuing the real `$27 $0B`. Don't confuse the enumeration sweep with the actual unlock — the unlock is the SINGLE `$27 $0B` request that follows.
- `hCLL=1` is the SAAB diagnostic link; `hCLL=2` is a parallel link (probably MS-CAN); `hCLL=5` is OBD-II/EOBD (used for `$7E0/$7E1`). Most interesting traffic is on `hCLL=1`.
- `pCoPTag` at offset 8 is consistent per-CLL: `0x0158839C` for `hCLL=1`, `0x015883A0` for `hCLL=2`, `0x0158926C` for `hCLL=5`. Useful as a sanity check that the CLL field is being read correctly.
- `PDUStartComPrimitive`'s `CoPType=0x8004` is what carries diagnostic requests in Chipsoft's implementation (NOT the standard `0x8010 PDU_COPT_SENDRECV`). Other observed types: `0x8001`, `0x8003`, `0x8011`, `0x8020`. They behave like `STARTCOMM`, `STOPCOMM`, etc., but their exact meaning isn't fully RE'd. Worth investigating later but not in the critical path.
- `$Level` byte numbering reminder (GMW3110 §8.8.2.1):
  - `$01/$02` = SPS programming (Trionic.NET-solved)
  - `$03/$04` = DevCtrl
  - `$05–$0A` = Reserved-must-not-use
  - `$0B–$FA` = Vehicle-manufacturer-specific (where SAAB lives — `$0B` confirmed)
  - `$FB–$FE` = ECU/supplier manufacturing
  - Odd = requestSeed, even = sendKey. So after `$27 $0B` we'll see `$27 $0C` carrying the key.

## Don't

- Don't recommend `LogLevel:1` (driver-side Boost.Log sink). It was investigated and found unstable. Memory: `project_chipsoft_loglevel1_mothballed.md`.
- Don't suggest CANHacker GUI / canscan.exe. They caused live-car bus disturbance and aren't on the critical path. The Python listen-only sniffer at `tools/chipsoft_canhack_capture.py` is the safe alternative if a bus capture is ever wanted, but it's secondary to the shim.
- Don't push without testing. The user (Chris Drews, `djfremen`) has a Win10 box running Tech2Win against a live SAAB and is the only one who can validate. Tightly-scoped commits are appreciated.
- Don't bulk-commit the parent `Chipsoft_RE/` directory if you're working from the parent `saab-security-access` workspace. `Chipsoft_RE` is its own git repo with its own remote (`github.com/djfremen/Chipsoft_RE.git`) — push there directly.
