# TrionicCANFlasher "Read ECM" — full operation decoded

**Source:** `Chipsoft_RE/notes/captures/2026-05-08-j2534-trioniccanflasher-readecm.pcap` (43 MB USBPcap of TrionicCANFlasher driving Chipsoft J2534 Pro adapter against an ECM bench).

**Decoded:** 2026-05-13 via `/tmp/decode_chipsoft_v2.py` (USBPcap → chipsoft envelope → ISO-TP PCI → scapy GMLAN).

**Scale:** 110,972 USB frames decompose into:
- 105,633 chipsoft-envelope-bearing frames (commit OUT + msg-available IN)
- 12,534 paired queue/commit OUT (real UDS sends)
- ~93k IN frames (mostly device-internal poll responses + multi-frame ISO-TP CF stream)

## Phase breakdown — what TrionicCANFlasher actually does

| Wall-clock (ms) | Phase | Description |
|---|---|---|
| 53400-53900 | adapter init | Chipsoft USB control commands (opcodes 0x08, 0x01, 0x04, 0x17, 0x12, 0x05, 0x20 — each ×4) — adapter open, version read, channel connect, filter set |
| 53907-56945 | **DID sweep** | 39+ DIDs probed via `1A xx` on $07E0: `0x71/72/73/74/75/0F/95/99/0A/B4/08/C1-C6/97/0C/92/02/25/7C/9A/CB/CC/A0/98/01/03/04/07/2E/B9/24/96/9A` — pulling part numbers, calibration IDs, software versions. ~75 ms per DID. Builds full ECM identity card. |
| 56970+ | DPID subscribe | `aa 01 7a` ReadDataByPacketIdentifier — engine vitals stream |
| ~74011 | ReportProgrammedState | `RX e2 00 ...` (positive of `$A2`) — Trionic asks ECM what programming state it's in |
| ~74022 | **Enter programming mode** | `TX a5 01` then `a5 03` (`$A5` = ProgrammingMode, sub 0x01 then 0x03) — drops engine into programming session |
| ~74108 | TesterPresent | `TX 3e → RX 7e` |
| **74196-74324** | **SecurityAccess L01** | `TX 27 01 → RX 67 01 7e 11` (seed 0x7E11), `TX 27 02 45 78 → RX 67 02` (key 0x4578, accepted). Algo low-byte 0x39 per prior mining. |
| 74483-74485 | **RequestDownload** | `TX 34 00 00 00 00 00 → RX 74 00 ...` — `$34` GMW3110 RequestDownload accepted |
| 74496+ | **ISO-TP CF stream** | Host streams a multi-KB blob to the ECM as ISO-TP First-Frame + Consecutive-Frames (5500+ CFs cycling PCI 0x21 → 0x2F). This is Trionic's "loader" script being uploaded to the ECM. |
| (continues for tens of seconds) | flash dump | After loader runs, ECM bulk-streams its flash contents back — 4500+ ms with ~4 KB/sec throughput as paired CF frames flow in both directions. |

## What the J2534 shim would add over this pcap-level view

The pcap gives us the **wire** level — every byte on the USB. The
J2534 shim would give us the **API** level on top:

1. **`PASSTHRU_MSG.Timestamp`** — the chipsoft adapter does have a
   hardware timestamp embedded in its USB envelope (we saw a varying
   counter at ofs 14-17 of some IN frames, ~1 µs:1ms ratio with
   wall-clock). But the offset is **format-dependent** — message-bearing
   IN frames put it elsewhere than control replies. Decoding it
   reliably from USB requires per-message-type unpacking. The J2534
   API exposes it as a single uint32 field on every `PASSTHRU_MSG`,
   no envelope-decoding needed.

2. **`PassThruIoctl(SET_CONFIG, ...)`** — we see Chipsoft control
   commands (opcodes 0x04, 0x08, 0x12, 0x17 etc.) without knowing
   what J2534 IOCTL they correspond to. The shim would log
   `IOCTL_NAME(P1Min, P2Max, P3Min, ...)` directly.

3. **`PassThruStartMsgFilter`** — we see a 79-byte OUT during init
   (`17 00 47 00 ...`) but can't tell which CAN-IDs Trionic asked the
   adapter to allow through. The shim shows it as `Filter(type=PASS,
   mask=..., pattern=..., flowControl=...)`.

4. **`PassThruReadVersion`** — we see the ASCII reply `c1 06 CHIPSOFT
   J2534 Pro v. 1.5.2`. The shim labels it.

5. **API-call vs USB-transfer dedup** — the pcap shows queue + commit
   as TWO USB frames per UDS send. The shim shows one
   `PassThruWriteMsgs(msg, count=1)` call.

## Key takeaways

- **Trionic's "Read ECM" is a flash dump, not a parameter read.** The
  39+ DID sweep is just the identity preamble; the real work is the
  `$A5 03` programming-mode entry → SecurityAccess L01 → `$34`
  RequestDownload → CF-stream loader upload → bulk flash readout.
- **SecurityAccess L01 is on $07E0 with algo low-byte 0x39 — works
  offline, bench-validated.** This is the same pattern OpenSAAB
  documents in `commands/saab/security_access_l01_unlock.yaml`.
- **No SAAB SAS ($27 0B) and no $0241 traffic in this pcap** — Trionic
  goes through OBD-II only. Stays consistent with the prior 2026-05-11
  mining note: J2534 clients don't enter the Tech2Win SAS path.
- **The chipsoft USB envelope HAS a hardware timestamp**, but the
  offset varies by message variant. The J2534 shim normalises this.

## What to do with this

- Build the j2534_interface.dll shim (mirror of CSTech2Win shim
  infrastructure) so we get the same kind of API-named timeline for
  ANY J2534 client (Trionic, OpenPort, BiSCAN, etc.) without having
  to USB-decode every capture.
- The `$A5 03` programming-mode entry + `$34` RequestDownload pair is
  a missing OpenSAAB workflow — should be captured as
  `commands/saab/engine_program_mode_entry_a5.yaml` and
  `commands/saab/request_download_34.yaml` from a fresh shim capture
  (cleaner than reverse-engineering it from this USB pcap).
