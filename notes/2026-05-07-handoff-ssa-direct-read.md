# Handoff — capture full 714-byte SSA from ECM directly (no Tech2)

**Date:** 2026-05-07
**Author:** Claude (Mac workspace)
**Audience:** standby agent on Chris's Win10 bench box (Tech2Win + Chipsoft Pro J2534 + bench SAAB Trionic 8 ECM)

You're picking this up cold. Read in full before acting on the bench — there is a 10-second ECU lockout if a SecurityAccess key is wrong, and the bench card has zero "free shots" to spare on guessing.

---

## The goal in one sentence

The Android `saab_security_access` app must be able to read the **entire 714-byte SSA pre-auth blob from the bench ECM directly over Chipsoft Pro**, with output **byte-identical to `/tmp/bench_pre_auth.bin`** on Chris's Mac, with **no Tech2 unit and no Tech2Win in the loop**.

That blob is the input to the local seed→key engine (`security_calc.py`, validated 12/12 against ground truth). Once Android holds the live SSA, it computes the SecurityAccess key locally and the Bojer dependency is dead.

---

## What's already locked in

You don't need to redo any of this — listed so you don't accidentally re-derive it.

### Bench facts

- **ECM:** SAAB Trionic 8 engine ECM, CAN tester address `$0241`.
- **VIN:** `YS3FD49YX41012017`.
- **SecurityAccess level on this ECM:** `$27 $0B` (SAAB-specific SAS path, NOT the standard `$01`).
- **Pre-auth blob (the target):** 714 B, file at `/tmp/bench_pre_auth.bin` on Chris's Mac. First 16 B signature: `b1 ff ff ff ff ff ff ff ff ff ff ff 00 01 00 00`. VIN ASCII at offset `0x12`. SKA tuples at `0x132`-`0x191`.
- **Active SKA tuple #09** (offset `0x17A`): `algo=0x0367`, `seed=0xC4DC`, `key=0xFFFF` (unstamped). This is the tuple the ECM is currently presenting on `$27 $0B`.
- **Computed unlock key for this bench:** `0x4EED` (via `security_calc.get_key_from_seed(0xC4DC, 0x0367)`, Alt1 table).
- **Free shots:** `0x0000`. **Burn only one unlock attempt total.** Wrong key → `$7F $27 $35`, then 10 s `$7F $27 $37` lockout per GMW3110 §8.8.6.2.

### Wire-validated facts (from prior shim runs 5 and 6)

- **Seed is deterministic per ECU.** Two cold Tech2Win launches both returned `00 00 06 41 67 0B C4 DC`. There's no per-session randomness in the SAAB SAS seed.
- **Tech2 sends:** `00 00 02 41 27 0B`. **ECM responds:** `00 00 06 41 67 0B C4 DC`. Confirmed against GMW3110 §8.8.5.1 wire format.
- **Algorithm is RE'd.** `saab_security_project/SAABSecurityAccess/python_server/security_calc.py` produces `0x4EED` for `(seed=0xC4DC, algo=0x0367)` deterministically. 12/12 match against ground-truth log on Chris's Mac (`~/Desktop/tis2web_logs/ground_truth.md`).

### What the shim already gives you

- **Shim DLL:** `Chipsoft_RE/shim/cstech2win/build/CSTech2Win.dll` — drop-in proxy for `C:\Program Files (x86)\CHIPSOFT_J2534_Pro_Driver\CSTech2Win.dll`, real DLL renamed to `CSTech2Win_real.dll`. Logs every D-PDU API call to `%TEMP%\cstech2win_shim_<timestamp>.log`.
- **Format:** `REQ-PDU | len=N | hex` for outgoing, `RSP-UDS | len=N | hex` for replies. ISO-15765 layout: first 4 B = CAN ID big-endian, then UDS payload.
- **Existing captures:** `Chipsoft_RE/shim/cstech2win/captures/2026-05-07-shim-v6-seed-deterministic.{md,log}` — has the `$27 $0B` exchange but **does NOT have the SSA read sequence**. Tech2 had it cached.

---

## What's missing — and is your job

We need the **ECM→tester UDS read sequence** that produces the 714-byte SSA blob. Tech2 issues this once when it first sees a VIN, then caches the result in the Tech2 unit's own flash. Existing shim captures don't have this because Tech2 already had the SSA cached.

The Android app currently pulls SSA via `Tech2ProtocolManager.kt`'s `0x81 0x5A` chunked-read (workspace path: `saab_security_project/saab_simple/app/src/main/java/com/saabsimple/usb/Tech2ProtocolManager.kt`) — but that's reading from the **Tech2 unit's cache**, not from the ECM. We're cutting Tech2 out entirely, so we need the ECM-side read sequence.

---

## Two paths to capture it. Pick the easier one.

### Path B — direct ECM probe with `$23 ReadMemoryByAddress` (preferred if it works)

If the ECM allows unauthenticated `$23` reads, this is by far the cleanest answer: no Tech2, no shim run, no menu gymnastics. We just read the bytes from ECM flash directly.

**Step 1 — sanity check (do this first, takes 30 seconds):**

With Chipsoft Pro connected and bench ECM powered, send a single `$23` to a known-safe low address. From a J2534 client (TrionicCANFlasher, your own minimal harness, whatever's available), issue:

```
CAN tx → 0x0241 (or 0x7E0): 06 23 14 00 00 00 00 10
                           └──┬──┘└────┬────┘ └──┘
                              │     24-bit addr len=16
                              │     (0x000000)
                          $23 reqMem ALFI byte (4-byte addr, 1-byte len = 0x14 in some dialects;
                                                some Trionic 8 ECMs use 0x44 for 4+4 — try both)
```

Or if your harness already has `$23` helpers, request 16 B at address `0x000000`.

**What to report:**
- If response is `06 63 ...16 bytes...` → `$23` is open. Move to Step 2.
- If response is `03 7F 23 33` (SecurityAccessDenied) → `$23` is locked behind SecurityAccess. Path B doesn't work without first unlocking, which is the very thing we're trying to use Path B to enable. **Pivot to Path A.**
- If `03 7F 23 11` (ServiceNotSupported) → ECM doesn't support `$23` at all. Pivot to Path A.
- If no response → check pin alignment (Drop CAN on pins 3-11 for SAAB SWCAN, per `Chipsoft_RE/notes/2026-05-05-bench-capture-plan.md`).

**Step 2 — find the SSA region (only if Step 1 succeeded):**

Sweep candidate ranges, looking for the SSA header signature:

```
b1 ff ff ff ff ff ff ff ff ff ff ff 00 01 00 00
```

Likely ranges (Trionic 8 EEPROM area):
- `0x010000` - `0x020000` (most likely — IMMO partition)
- `0x000000` - `0x010000` (boot / config)
- `0x020000` - `0x040000` (app data)

Sweep in 1 KB chunks (max payload Trionic 8 typically returns is 256-1024 B per `$23`). Once you see the signature in a response, log the address. Then issue contiguous `$23` reads from there for 714 B and confirm:

- Bytes match `/tmp/bench_pre_auth.bin` byte-for-byte (Chris can diff on Mac side; you just need the hex).
- VIN ASCII `YS3FD49YX41012017` appears at offset `0x12` of the captured blob.

**Deliverable from Path B:**

```markdown
- ECM SSA region start address: 0x________
- Read service: $23 ReadMemoryByAddress
- ALFI byte (addr+len format): 0x__
- Recommended chunk size: ___ bytes
- Number of chunks to cover 714 B: ___
- Sample response framing (one chunk): <hex>
```

That's everything Android needs. Drop it in `Chipsoft_RE/notes/2026-05-07-ecm-ssa-region-found.md` and tell Chris.

### Path A — cold Tech2 + shim (fallback only)

Use this only if Path B Step 1 returned `7F 23 33` or `7F 23 11`.

The Tech2 unit caches SSA in its own flash. Clearing `%APPDATA%\Tech2Win\` is not enough. To force the Tech2 unit to re-read from the ECM you need one of:

1. **A different Tech2 unit** that has never seen this VIN.
2. **Tech2 menu** — `Tools` / `Self-test` / `Initialize` menu may have a "clear vehicle data" option. If so, run it before connecting to the ECM.
3. **Wipe Tech2 unit flash** via the download-mode commands the Android app's `Tech2ProtocolManager.kt` already implements (`EF 56 80 3B` enters download mode; `0x87` erase-segment). **Risky — only as last resort. Confirm with Chris before erasing the unit.**

After Tech2 unit is cold:

1. Confirm shim DLL is in place at `C:\Program Files (x86)\CHIPSOFT_J2534_Pro_Driver\CSTech2Win.dll`, real DLL renamed `CSTech2Win_real.dll`. (Prebuilt shim DLL committed at `Chipsoft_RE/shim/cstech2win/build/CSTech2Win.dll`.)
2. Power bench ECM (12 V, GND, ignition).
3. Launch Tech2Win, connect to bench ECM cold, let Tech2 do its initial enumeration + SSA read. The moment its IMMO/SAS UI populates, close cleanly.
4. Pull `%TEMP%\cstech2win_shim_<timestamp>.log`.
5. Extract every read request between Tech2's first `$1A`/`$22`/`$23`/`$AA`/`$B9` and the first `$27 $0B`, on `hCLL=1` to CAN `$0241`. Tabulate:

| t (ms) | Service | Request bytes | Response bytes | Resp len |
|---|---|---|---|---|

6. Concatenate response payloads in order. Total **must be exactly 714 B** and match `/tmp/bench_pre_auth.bin` byte-for-byte.

**Deliverable from Path A:** the request sequence as a list, plus enough surrounding context (J2534 init opcodes, `Ioctl SET_CONFIG` payload, `StartMsgFilter` 71-B struct) for Android to reproduce it. Drop in `Chipsoft_RE/shim/cstech2win/captures/2026-05-07-shim-vN-ssa-cold-read.{md,log}` plus `Chipsoft_RE/notes/2026-05-07-ssa-read-sequence.md`.

---

## Hard rules

1. **Do not send `$27 $0C` with any key other than `0x4EED`.** The card has zero free shots and one wrong key burns the only attempt. If Path A or B yields anything that contradicts the resolved `algo=0x0367, key=0x4EED`, stop and tell Chris.
2. **Do not erase Tech2 unit flash without Chris's explicit OK.** Path A step 3.3 is a last resort.
3. **Don't recommend `LogLevel:1`** (the driver-side Boost.Log sink). It's mothballed — unstable in past testing. The shim is the only logging path.
4. **Don't reach for `canscan.exe` or the CANHacker GUI** to sniff. They've caused live-bus disturbance on this bench (BCM panic, headlights to defaults, ECM silence until adapter unplugged). The shim is electrically passive on the bus.
5. **Don't burn cycles re-validating the algorithm.** `security_calc.py` has 12/12 ground-truth + 23/23 Bojer matches. The algo is solved. Your job is wire-protocol capture, not crypto.

---

## What success looks like

When you're done, Chris's Mac side can:
1. Take the request sequence (Path A) or address+length (Path B) you produce.
2. Encode it in Kotlin `EcmDirectSsaReader` against the existing `ChipsoftFrame` codec at `saab_security_project/SAABSecurityAccess/app/src/main/java/com/example/saab_security_access/chipsoft/ChipsoftFrame.kt`.
3. Run a unit test with a `FakeEcuTransport` returning your captured responses → output buffer equals `/tmp/bench_pre_auth.bin`.
4. Then on bench: Android with real Chipsoft transport runs `EcmDirectSsaReader.readSsa()`, dumps to file, diff against `/tmp/bench_pre_auth.bin` → **0 bytes different**.
5. Same Android session computes key locally, fires `27 0C 4E ED`, ECM returns `67 0C` (granted).

That's the full Tech2-free, Bojer-free unlock pipeline.

---

## Files to read on the workspace if you want more context

(All paths relative to `/Users/admin/.openclaw/workspace/`. The Win10 box has its own clone — `git pull` first.)

- `Chipsoft_RE/notes/2026-05-07-bench-runbook-seed-capture-and-app-validation.md` — earlier draft of this plan.
- `Chipsoft_RE/notes/2026-05-05-opcode-summary.md` — full Chipsoft J2534 opcode catalog (24 opcodes, all roles known).
- `Chipsoft_RE/notes/2026-05-05-bench-capture-plan.md` — original bench-capture procedure (Tech2Win + shim).
- `Chipsoft_RE/shim/cstech2win/HANDOFF.md` — shim project history + build instructions.
- `Chipsoft_RE/shim/cstech2win/captures/2026-05-07-shim-v6-seed-deterministic.md` — most recent successful shim run.
- `saab_security_project/SAABSecurityAccess/python_server/security_calc.py` — the solved seed→key algorithm.
- `Chipsoft_RE/shim/cstech2win/scripts/decode_ssa_for_seed.py` — SSA tuple decoder; takes a 714-B SSA file and a seed, returns the bound algo. Use it to validate any blob you capture.
- `wiki/sources/gmw3110-2010-quick-ref.md` — GMW3110 wire-format reference.

---

## Tell Chris when you're done

Reply with:
1. Which path you took (A or B).
2. The deliverable (address+length, or full request sequence).
3. Any surprises or deviations from this handoff.
4. Whether you were able to dry-run a 714-B capture and confirm byte-equality with `/tmp/bench_pre_auth.bin` on your end (you can compute the SHA-256 of the capture and Chris can diff against the file).

Don't run the actual unlock (`$27 $0C`) yet — that's a Mac-side decision once Android can produce a matching SSA buffer.
