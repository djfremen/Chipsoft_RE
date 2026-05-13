"""
Parse a CSTech2Win shim log into a structured timeline of REQ/RSP pairs.
Output: JSON list of {t_ms, dir, canId, uds_hex, uds_decoded}.

Shim log format (pipe-separated):
  TIMESTAMP|TID|TYPE|TAG|len=N|BYTES
  REQ-PDU bytes layout: 4-byte CAN ID big-endian + UDS payload
  RSP-UDS bytes layout: same
"""
import json, sys, re
from pathlib import Path

UDS_SERVICES = {
    0x10: ("DiagnosticSessionControl", {0x01:"default", 0x02:"programming", 0x03:"extended"}),
    0x11: ("ECUReset", {}),
    0x14: ("ClearDiagnosticInformation", {}),
    0x18: ("ReadDtcInformation", {}),
    0x1A: ("ReadDataByLocalId", {0x90:"VIN", 0x3F:"VIN(alt)", 0x9A:"ECU_present?"}),
    0x22: ("ReadDataByCommonId", {}),
    0x23: ("ReadMemoryByAddress", {}),
    0x27: ("SecurityAccess", {0x01:"reqSeed_lvl1", 0x02:"sendKey_lvl1",
                              0x0B:"reqSeed_SAS",  0x0C:"sendKey_SAS"}),
    0x28: ("DisableNormalMessageTransmission", {}),
    0x29: ("EnableNormalMessageTransmission", {}),
    0x3D: ("WriteMemoryByAddress", {}),
    0x3E: ("TesterPresent", {0x80:"suppressResp"}),
    0xA9: ("DefinePid", {}),
    0xAA: ("DynamicallyDefineDID", {}),
    0xAE: ("ResponseOnEvent", {}),
}

POSITIVE_OFFSET = 0x40  # response SID = request SID + 0x40

def decode_uds(b: bytes) -> str:
    if len(b) == 0: return "<empty>"
    sid = b[0]
    # Negative response: 7F SS NN
    if sid == 0x7F and len(b) >= 3:
        bad_sid = b[1]; nrc = b[2]
        bad_name = UDS_SERVICES.get(bad_sid, (f"SID_0x{bad_sid:02X}", {}))[0]
        nrc_names = {0x11:"serviceNotSupported", 0x12:"subFunctionNotSupported",
                     0x13:"invalidFormat", 0x21:"busyRepeatRequest",
                     0x22:"conditionsNotCorrect", 0x24:"requestSeqError",
                     0x31:"requestOutOfRange", 0x33:"securityAccessDenied",
                     0x35:"invalidKey", 0x36:"exceededAttempts",
                     0x37:"timeDelayNotExpired", 0x78:"responsePending"}
        return f"NRC {bad_name} {nrc_names.get(nrc, f'0x{nrc:02X}')}"
    # Positive response
    if sid >= 0x40:
        req_sid = sid - 0x40
        if req_sid in UDS_SERVICES:
            svc, sub = UDS_SERVICES[req_sid]
            if len(b) >= 2:
                sub_name = sub.get(b[1], f"sub=0x{b[1]:02X}")
                return f"+{svc}.{sub_name} data={b[2:].hex(' ')}"
            return f"+{svc}"
    # Request
    if sid in UDS_SERVICES:
        svc, sub = UDS_SERVICES[sid]
        if len(b) >= 2:
            sub_name = sub.get(b[1], f"sub=0x{b[1]:02X}")
            return f"{svc}.{sub_name} data={b[2:].hex(' ')}"
        return svc
    return f"unknown SID 0x{sid:02X}"

def parse(path: Path) -> list[dict]:
    rows = []
    for raw in path.read_text(errors="ignore").splitlines():
        m = re.match(r"^(\d+)\|(\d+)\|(\w+)\s*\|([A-Z\-]+)\|len=(\d+)\|(.+)$", raw)
        if not m: continue
        t_ms, tid, fmt, tag, blen, body = m.groups()
        if tag not in ("REQ-PDU", "RSP-UDS"): continue
        bs = bytes.fromhex(body.replace(" ", ""))
        if len(bs) < 4: continue
        can_id = int.from_bytes(bs[:4], "big")
        uds = bs[4:]
        rows.append({
            "t_ms": int(t_ms),
            "tid": int(tid),
            "dir": "TX" if tag == "REQ-PDU" else "RX",
            "can_id": f"0x{can_id:08X}".replace("0x0000", "0x"),
            "uds_hex": uds.hex(" "),
            "uds_decoded": decode_uds(uds),
        })
    return rows

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: parse_shim_to_timeline.py <shim.log> [output.json]")
        sys.exit(2)
    rows = parse(Path(sys.argv[1]))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if out:
        out.write_text(json.dumps(rows, indent=2))
        print(f"wrote {len(rows)} rows → {out}")
    else:
        for r in rows[:50]:
            print(f"t={r['t_ms']}  {r['dir']:2}  {r['can_id']:>9}  {r['uds_decoded']}")
        print(f"... ({len(rows)} total rows)")
