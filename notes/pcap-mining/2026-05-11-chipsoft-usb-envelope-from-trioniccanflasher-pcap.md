# Chipsoft USB wire envelope — derived from 2026-05-08 TrionicCANFlasher pcap

Source: `Chipsoft_RE/notes/captures/2026-05-08-j2534-trioniccanflasher-readecm.pcap` (42 MB, USBPcap).

USB topology: chipsoft = device 10. Bulk OUT `0x01` (host→device), bulk IN `0x81` (device→host).

## Wire envelope — confirmed byte layout

35-byte PassThruWriteMsgs-style envelope for a 2-byte UDS payload at one CAN ID:

```
ofs  bytes                value (this pkt)        meaning
0-1  22 00 / 0F 00        opcode                  0x22=queue, 0x0F=commit
2-5  1B 00 00 00          payload length          27 (LE u32)
6-7  1d 01 / 3f 01        checksum/CRC            depends on body
8-11 00 00 00 00          reserved                always 0 in queue
12-15 05 00 00 00         protocol id             5 = CAN
16-19 00 00 00 00 (q)     msgID slot              0 in queue
      17 0b 00 00 (c)                             commit echoes a chipsoft-assigned token
20-23 07 00 00 00         tx flags                fixed
24-29 00 00 00 00 00 00   padding                 zeros
30-31 07 e0               CAN ID (big-endian)     0x07E0 here
32    02                  ISO-TP PCI = SF len     UDS data length (2 here)
33-34 27 01               UDS payload             $27 $01
```

For a 4-byte UDS payload (e.g. `27 02 KK KK`), the envelope is **37 bytes** — only the trailing PCI+UDS section grows; offsets 0–31 stay the same.

## Complete unlock sequence captured

```
#4335 OUT len=35   ...07 e0 02 27 01        [queue $27 01]
#4338 OUT len=35   ...07 e0 02 27 01        [commit $27 01]
#4346 IN  len=39   ...07 e8 04 67 01 7e 11  [seed 0x7E11]
... host computes key via Trionic algo (low-byte 0x39) ...
#4371 OUT len=37   ...07 e0 04 27 02 45 78  [queue $27 02 key=0x4578]
#4374 OUT len=37   ...07 e0 04 27 02 45 78  [commit $27 02]
#4382 IN  len=39   ...07 e8 02 67 02        [ACK — unlock granted]
```

Algorithm validated: `security_calc.get_key_from_seed(0x7E11, algo & 0xFF == 0x39) == 0x4578`. 255 matching `algo_id` values (all those with low byte `0x39`), confirming our table-driven impl is correct for level $01.

## Android comparison

Android (`ChipsoftTransport.writeMsgQueue`) produces structurally identical bytes — same opcode, same length, same protocol id, same flags. The only differences for a working frame are the CAN ID (offset 30–31) and the body-dependent checksum (offset 6–7).

This means: **Android's USB framing is not the cause of the bench silence.** When Android sent `$27 01` to CAN `0x0241` it produced a well-formed chipsoft frame; the chipsoft accepted it and put it on the bus. The bench ECM simply did not respond on `0x0641`.

## Implications for the Android SAS path

1. **`$27 01` at `$07E0` is proven to work end-to-end via the J2534 / chipsoft path** — we have the byte-perfect template and a key-derivation algorithm that matches.
2. **`$27 0B` at `$0241` (Tech2Win SAS path) is NOT in this pcap.** TrionicCANFlasher's J2534 driver never sends to `$0241` and never uses level `$0B`. The 2026-05-07 CSTech2Win shim capture is the only evidence we have for that path, and it uses a different DLL (`CSTech2Win.dll`, D-PDU API) with possibly a different USB framing.
3. **Fastest path to a working Android unlock:** mirror the captured `$27 01 → $27 02` sequence exactly. Use `$07E0` as the target CAN ID, level `$01`, and `security_calc` for key derivation. We can do this today with the existing build.
4. **For SAS post-auth write-back** (the ultimate goal), `$27 0B` may still be required. To unblock that, we need either:
   - A new USBPcap capture of Tech2Win driving a complete SAS unlock on the bench (USB endpoint + CSTech2Win.dll shim running simultaneously), OR
   - Empirical test: try `$27 0B` at `$07E0` (instead of `$0241`) to see if the level-$0B service is reachable via OBD-II addressing.

## Files

- Parser: `/tmp/parse_usbpcap.py`, `/tmp/find_sas_frames.py`, `/tmp/full_seq.py`
- Source pcap: `Chipsoft_RE/notes/captures/2026-05-08-j2534-trioniccanflasher-readecm.pcap`
