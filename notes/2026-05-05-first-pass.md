# Chipsoft_RE — first-pass static analysis (2026-05-05)

Tooling: `pefile` + `capstone` (Python bindings) under `.venv/`. Scripts: `tools/pe_summary.py`, `tools/disasm_export.py`. Both DLLs are 32-bit (PE32 x86), MSVC C++ with thiscall member functions. Image base for both: `0x10000000`.

## Headline findings

### 1. The Chipsoft Pro device is a virtual COM port, not raw USB-bulk

`j2534_interface.dll` imports from `KERNEL32` include:

- `CreateFileA`, `CreateFileW`, `WriteFile`, `ReadFile`, `DeviceIoControl`, `CloseHandle` — file-handle I/O
- **`GetCommState`, `SetCommState`, `SetCommTimeouts`, `PurgeComm`** — *these are Win32 COM-port APIs*
- `CreateIoCompletionPort`, `GetOverlappedResult`, `GetQueuedCompletionStatus`, `PostQueuedCompletionStatus` — async overlapped I/O on the handle
- `SETUPAPI.dll` + `CM_Get_Device_IDA`, `CM_Locate_DevNodeA`, `CM_Get_Parent`, `SetupDiGetClassDevsA` — enumerates device interfaces (likely `GUID_DEVINTERFACE_COMPORT` to find `\\.\COMx`)

**No `WinUSB.dll`, no `libusb`, no `libusb0`, no HID/`hid.dll`.** The DLL talks to its hardware as a virtual COM port — i.e., USB-CDC ACM under the hood.

**Why this matters for an Android port**: the "vendor-proprietary USB framing" risk gate collapses. Android can speak to USB-CDC devices today via [`usb-serial-for-android`](https://github.com/mik3y/usb-serial-for-android). The remaining unknown is the *byte protocol on the serial pipe*.

`WS2_32.dll` is also imported (`WSAStartup`/`WSACleanup`), suggesting an optional TCP path or telemetry. Worth tracing but secondary.

### 2. `CSTech2Win.dll` is a D-PDU API library, not a Tech2-specific blob

29 exports, all prefixed `PDU*` — `PDUConstruct`, `PDUConnect`, `PDUCreateComLogicalLink`, `PDUStartComPrimitive`, `PDUIoCtl`, `PDUSetComParam`, etc. This is the ISO 22900-2 **D-PDU API** (the modern J2534 successor). The "Tech2Win" in the name refers to the **client app** that loads this DLL (Chipsoft's Tech2 emulator), not to Tech2 internals.

Implication: this DLL probably does *not* contain the SAAB SKA / SecurityAccess key derivation. It's the transport-level driver, not the application-protocol library. Need to look at Tech2Win.exe itself (not in this drop) for the SKA/IMMO algorithm.

The post-auth structure recorded in `project_saab_genuine_tech2win_postauth_structure.md` (HWKID `S000310723`, 10 SKA tuples) was *output* of the genuine Chipsoft Tech2Win toolchain — the algorithm that generates it lives elsewhere in that toolchain.

## Export call shape

Every J2534 export is a 12-byte thiscall stub:

```asm
push ebp
mov  ebp, esp
call 0x10006f40        ; → returns context pointer in eax
mov  ecx, eax          ; ecx = this
pop  ebp
jmp  0x10004f20        ; tail-call into the real method
```

So `0x10006f40` is the singleton/context accessor; the real implementations live at:

| Export | Real impl |
|---|---|
| PassThruOpen          | (only stub disasm'd so far — leads to `0x10004a00`) |
| PassThruConnect       | `0x10004f20` |
| PassThruDisconnect    | `0x100051d0` |
| PassThruReadMsgs      | `0x10005390` |
| PassThruWriteMsgs     | `0x10005680` |
| PassThruStartPeriodicMsg | `0x10005970` |
| PassThruIoctl         | `0x100070a0` |

Trace one of these (`PassThruWriteMsgs` is the highest-signal target — that's the path to the wire) to find the `WriteFile`/`DeviceIoControl` call sites and the byte format being shipped.

## Open questions for next pass

1. Where does `j2534_interface.dll` open the COM port? Find the `CreateFileA`/`CreateFileW` call site and look at what's pushed onto the stack for the path string. It probably builds `\\.\COMx` from a registry/SetupAPI lookup.
2. Does it use any non-trivial `DeviceIoControl` ops, or pure read/write/comm-state? Pure read/write ⇒ a clean clone-able byte protocol.
3. What does `PassThruWriteMsgs` actually emit on the wire for a CAN frame? Disassemble `0x10005680` and chase down to `WriteFile`.
4. Is there a config string / VID:PID hint in `.rdata`? Strings dump would answer.

## Workflow recap

```bash
cd Chipsoft_RE
.venv/bin/python tools/pe_summary.py     CHIPSOFT_J2534_Pro_Driver/j2534_interface.dll
.venv/bin/python tools/disasm_export.py  CHIPSOFT_J2534_Pro_Driver/j2534_interface.dll PassThruWriteMsgs
.venv/bin/python tools/disasm_export.py  CHIPSOFT_J2534_Pro_Driver/j2534_interface.dll 0x10005680 --bytes 0x800
```

For multi-file dives, Ghidra (free, scriptable) on top of these scripts is the right next step. Capstone is fine for targeted disassembly; Ghidra is the call-graph + decompiler.
