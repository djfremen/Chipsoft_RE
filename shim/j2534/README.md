# j2534_interface shim

DLL shim that intercepts calls to `j2534_interface.dll` (the SAE J2534
PassThru API exposed by the Chipsoft J2534 Pro adapter) and logs every
instrumented call to `%TEMP%\j2534_shim_<timestamp>.log`.

Companion to the `cstech2win` shim. Both can be deployed simultaneously
on the same host — Tech2Win loads `CSTech2Win.dll`, J2534 clients
(TrionicCANFlasher, OpenPort, BiSCAN, etc.) load `j2534_interface.dll`.
Each writes its own log file timestamped with wall-clock so they can
be merged after the fact.

## Build

On the EliteBook (32-bit MSVC required because the real DLL is PE32 x86):

```
cd shim\j2534
python3 scripts\gen_shim.py "C:\Program Files (x86)\CHIPSOFT_J2534_Pro_Driver\j2534_interface.dll"
python3 scripts\fix_msvc.py
scripts\build_msvc.bat
```

Output: `build\j2534_interface.dll` (~30 KB).

## Install

```
cd "C:\Program Files (x86)\CHIPSOFT_J2534_Pro_Driver"
move j2534_interface.dll j2534_interface_real.dll
copy <wherever>\build\j2534_interface.dll .\
```

The shim's `DllMain` will `LoadLibrary("j2534_interface_real.dll")` and
resolve all 14 PassThru* exports against it on first attach.

## Instrumented vs forwarded

| Function | Mode | Why |
|---|---|---|
| PassThruOpen          | log args + ret | adapter handshake |
| PassThruConnect       | log args + ret | protocol + baud + channel ID |
| PassThruIoctl         | log args + ret | config / clear / batt / init ops |
| PassThruStartMsgFilter| log args + ret | filter type, mask, pattern, flow ctl |
| PassThruWriteMsgs     | log args + ret | TX side (UDS / CAN data) |
| PassThruReadMsgs      | log only when `Got > 0` | RX side incl. hardware Timestamp |
| PassThruClose, Disconnect, ReadVersion, GetLastError, SetProgrammingVoltage, StartPeriodicMsg, StopMsgFilter, StopPeriodicMsg | naked-jmp forwarder | not interesting; just pass through |

## Log format

Pipe-delimited:

```
<ms_since_attach> | <wall_clock_ms> | <tid> | <event_class> | <fn_name> | <detail>
```

`wall_clock_ms` is FILETIME / 10000 — directly comparable against the
cstech2win shim's wall_clock_ms column for cross-shim merge.

For TX/RX messages, the next line is a `HEX` row with the actual
PASSTHRU_MSG.Data bytes:

```
1234|1715661234567|7890|HEX  |TX[0]|len=2|27 01
```

## Decoder

Use `tools/j2534_log_decode.py` (sister of `shim_log_decode.py`) to
render a clean UDS timeline.
