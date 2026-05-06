# options.json — answers from static RE

Built from `2026-05-05-ghidra-{config,config-readers,logpath,init}.md`.
All conclusions below are derived from `j2534_interface.dll` static analysis;
no runtime / network info needed.

## TL;DR

| Question | Answer |
|---|---|
| **What LogLevel value enables logging?** | **`0..4` enables; `≥5` disables.** Default 10 = off. **Use `0` for max verbosity (trace).** |
| **Where does the log file land?** | **`%ALLUSERSPROFILE%\CHIPSOFT_J2534\logs\<YYYYMMDD>_<HHMMSS>.log`** = on Win10 default: `C:\ProgramData\CHIPSOFT_J2534\logs\…`. |
| **What other config keys exist?** | Top-level: `LogLevel`. Per-tier sub-objects: `Lite`, `Mid`, `Pro`. Inside each tier: `OpenPort2Mode`, `RemapAUXToPIN`, `SplitReadTimeout`. |

## 1. LogLevel scale (definitive)

The log-sink builder is `FUN_10011a99`, decompiled in
`2026-05-05-ghidra-logpath.md`. The first line of the body is the gate:

```c
if (*(byte *)(unaff_EDI + 0xc) < 5) {
    // build path, register Boost.Log file sink, set Severity filter
    ...
    bVar1 = *(byte *)(unaff_EDI + 0xc);
    uVar4 = FUN_1006b4b0((PSRWLOCK)"Severity");
    *(uint *)(unaff_EBP - 0x318) = (uint)bVar1;
    FUN_10021420(...);                              // sets the sink's
                                                    // severity threshold
}
```

`unaff_EDI` is the config object pointer; `+0xc` is the `LogLevel` field
(byte). Boost.Log's standard severity-level enum is `[trace=0] [debug=1]
[info=2] [warning=3] [error=4]` — exactly the five labels we see in the
DLL's strings.

**Therefore:**

| LogLevel | Effect |
|---|---|
| **`0`** | sink created; threshold = trace. **Captures everything**, including the `(W) >> ` / `(R) << ` wire markers (these are at trace level). |
| `1` | sink created; threshold = debug. Captures debug + info + warning + error. May still capture wire markers. |
| `2`–`4` | progressively quieter. |
| `≥ 5` | **no sink created at all.** No log file. |

Default `10` (per existing notes) = no log, since 10 ≥ 5.

**Recommendation: set `LogLevel: 0` for the bench session.** Guarantees the
wire-byte markers land in the file regardless of their internal severity.

## 2. Log file path (definitive)

Path is built at DLL load by `FUN_10010550` (the giant init function;
`2026-05-05-ghidra-init.md` lines 426-516):

```c
puVar14 = (uint *)FUN_100a6254("ALLUSERSPROFILE");      // getenv()
...
FUN_100030d0(local_330, puVar14, ...);                  // local_330 = $ALLUSERSPROFILE
puVar14 = FUN_10002e90(local_330, &DAT_100e087c);       // append "\"
puVar14 = FUN_10020fb0(&local_2e0,
                       &ppppuStack_2fc,
                       &DAT_100fcd38);                  // append global std::string …
puVar14 = FUN_10002e90(puVar14, &DAT_100e087c);         // append "\"
```

Where:
- `getenv("ALLUSERSPROFILE")` returns `C:\ProgramData` on a default Win10 install.
- `DAT_100e087c` = `0x5C 0x00 0x00 0x00` — a one-byte string holding `\` (the path separator). Confirmed by raw hexdump of the .rdata constant.
- `DAT_100fcd38` and the related `DAT_100fcce8` are global `std::string`
  objects that get populated at DLL load by the CRT static initializers
  (visible at file offsets `0x713`, `0xa93`, `0xe23` — three blocks for
  Lite/Mid/Pro tiers). The relevant assignments:
  - `0x100fccc0` = `"LogLevel"`
  - `0x100fccd0` = `"RemapAUXToPIN"`
  - `0x100fcce8` = `"CHIPSOFT_J2534"` (the subdirectory name)
  - `0x100fccf0` = `"SplitReadTimeout"`
  - `0x100fcd08` = `"Pro"`
  - `0x100fcd20` = `"OpenPort2Mode"`
  - `0x100fcd38` = `"options.json"`
  - `0x100fcd50` = `"Lite"`

After the init concatenation chain plus the log-builder's `\logs\` and
`%Y%m%d_%H%M%S.log` (from `FUN_10011a99`), the final path is:

```
%ALLUSERSPROFILE%  \  CHIPSOFT_J2534  \  logs  \  YYYYMMDD_HHMMSS  .log
       │             │       │          │              │
       └─ getenv     └─ "\"  └─ DAT     └─ "\"          └─ Boost.Log
                              _100fcce8                   timestamp
```

Default on Win10: **`C:\ProgramData\CHIPSOFT_J2534\logs\<timestamp>.log`**.
The format inside each line is `[%TimeStamp%]: %Message%` (also confirmed
in the FUN_10011a99 decompile).

The `options.json` config file itself lives at the parallel path
**`C:\ProgramData\CHIPSOFT_J2534\options.json`** — same base, no `\logs\`
subdir.

## 3. Full config-key set (definitive)

The CRT static initializers explicitly construct these `std::string` keys
(no others were found anywhere in the binary):

**Top-level:**
- `LogLevel` — integer `0..4` enables (threshold), `≥5` disables sink.

**Tier sub-objects** (three of them — once per device tier):
- `Lite`
- `Mid`
- `Pro`

**Keys inside each tier:**
- `OpenPort2Mode` — boolean. (Per existing operational note, set true for Pro to enable the second virtual COM port.)
- `RemapAUXToPIN` — integer pin number. (Existing note: `12` for Pro.)
- `SplitReadTimeout` — integer milliseconds.

Three identical-structure CRT initializer blocks (file offsets `0x713`,
`0xa93`, `0xe23`) construct three independent sets of these strings, one
for each tier. This locks down the JSON layout.

**Inferred options.json schema:**
```json
{
  "LogLevel": 0,
  "Lite": { "OpenPort2Mode": false, "RemapAUXToPIN": 0,  "SplitReadTimeout": 0 },
  "Mid":  { "OpenPort2Mode": true,  "RemapAUXToPIN": 0,  "SplitReadTimeout": 0 },
  "Pro":  { "OpenPort2Mode": true,  "RemapAUXToPIN": 12, "SplitReadTimeout": 0 }
}
```

(Defaults shown are best-guesses based on the operational config Chris
already had on hand; the binary doesn't hard-code these — `boost::ptree`
returns whatever the file contains.)

The Chipsoft Pro device is the relevant tier for the J2534 driver →
**only the `Pro` sub-object's settings affect Tech2Win's behavior** for
our use case.

## What we still don't know from static RE alone

1. **Whether `LogLevel: 0` actually captures the `(W) >>` / `(R) <<`
   markers**, or whether those are emitted at a higher severity that's
   always-on. The decompile shows the threshold is the LogLevel value,
   but doesn't tell us the severity tag of the markers themselves.
   Answer: try `LogLevel: 0` first; if the file is empty of `(W)` /
   `(R)` lines, escalate to a Ghidra script that traces back from each
   `(W) >> ` string ref to its `BOOST_LOG_SEV(_, severity)` call site.
2. **Boolean vs integer encoding for `OpenPort2Mode`**. JSON `true` /
   `false` works because `boost::ptree` parses both `true` and `1` for
   booleans, but the binary expects an integer at the C side. Existing
   note used `true` and it worked, so this is settled in practice.
3. **What `OpenPort2Mode` actually does at runtime.** The string is the
   key name; the C-side handler hasn't been chased yet. Not relevant to
   bench capture.

## Files used to derive this

- `Chipsoft_RE/notes/2026-05-05-ghidra-config.md` (auto)
- `Chipsoft_RE/notes/2026-05-05-ghidra-config-readers.md` (auto)
- `Chipsoft_RE/notes/2026-05-05-ghidra-logpath.md` (auto)
- `Chipsoft_RE/notes/2026-05-05-ghidra-init.md` (auto)
- `Chipsoft_RE/tools/ghidra_scripts/Dump{Config,ConfigReaders,LogPath,Init}.java` (re-runnable)
