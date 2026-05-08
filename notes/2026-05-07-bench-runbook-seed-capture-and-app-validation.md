# Bench runbook — full 714-byte SSA capture from ECM (2026-05-07)

**Big-picture goal (Chris, 08:31 HST):** the Android app must read the **entire 714-byte SSA pre-auth blob from the ECM directly** — by issuing the right diagnostic read sequence over Chipsoft Pro and capturing the bytes off the wire. The result must be **byte-identical to `/tmp/bench_pre_auth.bin`** (the file extracted from Tech2Win for VIN `YS3FD49YX41012017`). No Tech2Win in the production path.

This subsumes the seed-capture work. The `$27 $0B` SecurityAccess seed (`0xC4DC`) is *downstream* of having the SSA — once the Android app has the SSA in hand, it decodes (`decode_ssa_for_seed.py`) → maps `(seed → algo)` → computes key (`security_calc.get_key_from_seed`) → sends `27 0C 4E ED` → ECM unlocks.

## Two passes

- **Pass A — capture Tech2Win's full SSA-read sequence with the shim.** Until we have the *list of UDS requests* Tech2 issues to dump 714 bytes of IMMO/SSA region, the Android app has no script to replay. Run 5/6 captures don't include this — Tech2 had it cached. Pass A's deliverable is the ordered list of `$1A` / `$22` / `$23` (and possibly `$B9`) requests + their responses, totalling 714 bytes of payload.
- **Pass B — Android replays that sequence over Chipsoft Pro and dumps the result.** Compare byte-for-byte against `/tmp/bench_pre_auth.bin`. 100 % match = end-to-end validated; the app no longer depends on Tech2Win or Bojer.

---

## Bench facts

- ECM: SAAB Trionic 8 engine ECM, CAN `$0241`
- VIN of bench card: `YS3FD49YX41012017`
- Pre-auth SSA: `/tmp/bench_pre_auth.bin` (714 B, fetched 2026-05-07 from Chris's Drive)
- Tuple #09 @ 0x17A: `algo=0x0367`, `seed=0xC4DC`, `key=0xFFFF` (unstamped)
- Computed key (Alt1 table): **`0x4EED`**
- Free shots: `0x0000` — burn one attempt only
- ECU lockout: 10 s `RequiredTimeDelayNotExpired` after a bad key (`$7F $27 $37`)

---

## Pass A — capture Tech2Win's SSA-read sequence (the big one)

This is the missing piece. The shim runs 5 / 6 only cover the `$27 $0B` seed exchange because Tech2 had the SSA cached. To force a fresh read of all 714 bytes, the bench session must start cold.

### Force a cold SSA read

1. Win10 box, Chipsoft Pro plugged in, shim DLL in place at `C:\Program Files (x86)\CHIPSOFT_J2534_Pro_Driver\CSTech2Win.dll`, real DLL renamed `CSTech2Win_real.dll`.
2. **Clear Tech2Win's local cache** so it must re-read SSA from the ECM:
   - `%APPDATA%\Tech2Win\` — delete or rename any `*.bin` / `*.ssa` / VIN-named files
   - `%TEMP%\Tech2Win*` — same
   - If Tech2Win has an in-app "Forget vehicle" / "Reset" option, use it
3. Power bench ECM (12 V, GND, ignition).
4. Launch Tech2Win, connect to the bench ECM **fresh** — i.e., let it read VIN, read SAS state, read SSA. You will see in the shim log a long burst of `REQ-PDU` lines on `hCLL=1` to CAN `$0241` carrying `$1A` / `$22` / `$23` (and possibly `$B9`) requests, followed by `RSP-UDS` lines with the data.
5. The moment Tech2's IMMO/SAS UI shows the unlocked-state info populated, **close cleanly**. Pull `%TEMP%\cstech2win_shim_<timestamp>.log`.

### What to extract from the log

For every read request between Tech2's first `$1A`/`$22`/`$23` and the start of the `$27 $0B` SecurityAccess flow, write down:

| t (ms) | hCLL | CAN ID | Service | DID / address | Req bytes | Rsp bytes | Rsp len |
|---|---|---|---|---|---|---|---|

Concatenate the response payloads in order — total should be exactly **714 bytes**. Confirm byte-for-byte against `/tmp/bench_pre_auth.bin`. (`/tmp/bench_pre_auth.bin` starts: `b1 ff ff ff ff ff ff ff ff ff ff ff 00 01 00 00 00 00 ff ff` then ASCII VIN at +0x10. Find that signature in the concatenated reads.)

### Why a "longer log that includes init / filter / SET_CONFIG calls" is also needed

The Android app needs the J2534 init recipe (ProtocolID, baud, J1962_PINS, the `StartMsgFilter` 71-byte struct for CAN `$0641`) as well as the SSA-read PDU sequence. Pass A's log gives both — the shim sees every D-PDU layer call, including config-time ones. **Important:** also flag every `Ioctl` / `StartMsgFilter` line in the log; those go in Pass B's init prelude.

If the seed-exchange shim runs (5, 6) didn't already log SET_CONFIG/StartMsgFilter payloads, extending the shim's wrappers to dump them is a tiny edit — `wrappers.c` already has the typedefs from `gen_shim.py`. Decision deferred to whoever runs Pass A: grep first, extend shim only if needed.

Save the capture as `Chipsoft_RE/shim/cstech2win/captures/2026-05-07-shim-vN-ssa-cold-read.{md,log}` plus a separate `2026-05-07-ssa-read-sequence.md` with the request/response table.

---

## Pass B — Android replays the SSA-read sequence over Chipsoft Pro

Goal: Android app sends the same UDS read sequence captured in Pass A, concatenates the responses, and produces a 714-byte buffer that **byte-matches `/tmp/bench_pre_auth.bin`**.

Already built:
- `chipsoft/ChipsoftFrame.kt` — 8-byte LE header + payload + 16-bit additive checksum codec
- `SaabSecurityAccessPdu.REQUEST_SEED_0B = 00 00 02 41 27 0B`, `extractSeed0B(...)`

Still needed before Pass B can fire on the bench:
1. **J2534 init recipe** (from Pass A log):
   - opcode sequence on PassThruOpen: `0x20 → 0x01 → 0x08`
   - `PassThruConnect` ProtocolID + baud (host-side only, no wire opcode)
   - `PassThruIoctl SET_CONFIG`: ProtocolID, baud, J1962_PINS — payload bytes from Pass A
   - `PassThruStartMsgFilter` opcode `0x17`: full 71-byte struct from Pass A for CAN `$0641` (and any other ECU CAN IDs the SSA read touches)
2. **The SSA-read PDU sequence** (from Pass A): the ordered list of `$1A` / `$22` / `$23` / `$B9` requests + expected response framing.
3. **PassThruWriteMsgs opcode `0x22` payload layout** — 0x14 (20) bytes of header before the UDS payload, per `2026-05-05-opcode-summary.md`. Recover the struct layout from Pass A's `(W) >> 22 ...` lines.

**While the bench session is being scheduled, the standby agent can do without hardware:**

- Add a unit test under `app/src/test/java/.../chipsoft/` that asserts `ChipsoftCodec.encode` produces wire bytes matching shim log lines. Use existing run-6 capture for vectors.
- Build a `SsaReader` class that takes the (eventually populated) PDU sequence as an `Array<UdsRequest>`, fires each, accumulates responses, and emits a 714-byte buffer.
- Add a unit test that takes a recorded shim transcript JSON, fakes the ECM responses through a `FakeEcuTransport`, and asserts the final buffer equals `/tmp/bench_pre_auth.bin` byte-for-byte. Validates the read/concatenate logic before bench day.

**Sequencing once Pass A artifacts land:**
1. Android opens device, runs `0x20 → 0x01 → 0x08`.
2. Connect (host-side state only).
3. Ioctl SET_CONFIG with captured payload.
4. StartMsgFilter for CAN `$0641` (+ others).
5. For each read PDU in Pass A's sequence: WriteMsgs (0x22) with the request, ReadMsgs (0x10) for the response, append payload to buffer.
6. Compare buffer to `/tmp/bench_pre_auth.bin`. Must match all 714 bytes.
7. *(Then)* WriteMsgs `00 00 02 41 27 0B` → expect `00 00 06 41 67 0B C4 DC` → `extractSeed0B` → 0xC4DC → `security_calc.get_key_from_seed(0xC4DC, 0x0367)` → 0x4EED → WriteMsgs `00 00 04 41 27 0C 4E ED` → expect `67 0C` (granted).

---

## Decision gate

| Pass B SSA buffer | Action |
|---|---|
| 714 B, byte-identical to `/tmp/bench_pre_auth.bin` | ✓ Tech2Win-free SSA acquisition validated. Proceed to seed/key/unlock with `0xC4DC` → `0x4EED`. |
| 714 B but bytes differ | Compare diff: HWKID region? SKA tuple region? Tail? Likely a missed read or wrong DID. Iterate on Pass A list. |
| < 714 B / requests fail | Init recipe wrong (filter not catching, baud mismatch, PINS off). Diff Android wire bytes against shim `(W) >>` lines from Pass A. |

---

## Files referenced

- `Chipsoft_RE/shim/cstech2win/scripts/decode_ssa_for_seed.py`
- `saab_security_project/SAABSecurityAccess/python_server/security_calc.py`
- `saab_security_project/SAABSecurityAccess/app/src/main/java/com/example/saab_security_access/chipsoft/ChipsoftFrame.kt`
- `Chipsoft_RE/notes/2026-05-05-opcode-summary.md`
- `Chipsoft_RE/shim/cstech2win/captures/2026-05-07-shim-v6-seed-deterministic.md`
- `wiki/sources/gmw3110-2010-quick-ref.md`
