"""
Take a structured timeline (from parse_shim_to_timeline.py) and segment it into
named workflows by detecting transitions. Outputs a workflow catalogue entry.

Heuristics for boundaries:
  - $1A 9A on $0101 functional → "module_presence_scan"
  - $1A 90 sweep across $024X → "vin_sweep"
  - $27 01 sweep across $024X → "seed_sweep_l01"
  - $AA 01 01 to $0241 → "dynamic_did_setup"
  - $AE 00 to $0241 → "response_on_event"
  - $27 0B to $0241 → "engine_sas_seed"
  - $27 0C to $0241 → "engine_sas_key"
  - $3D to $0241 → "ssa_writeback"
  - $10 02/03 to $0241 → "session_change"
  - $3E 80 broadcast → "tester_present_wake"
"""
import json, sys, re
from pathlib import Path
from collections import OrderedDict

def detect_step_type(row):
    uds = bytes.fromhex(row["uds_hex"].replace(" ", "")) if row["uds_hex"] else b""
    if not uds: return "unknown"
    sid = uds[0]
    sub = uds[1] if len(uds) > 1 else None
    can = row["can_id"]

    if sid == 0x10 and sub in (0x02, 0x03):
        return f"diag_session.{['','','program','extend'][sub]}"
    if sid == 0x1A and sub == 0x90: return "read_vin"
    if sid == 0x1A and sub == 0x9A: return "ecu_presence_probe"
    if sid == 0x1A and sub == 0x3F: return "read_vin_alt"
    if sid == 0x27 and sub == 0x01: return "sec_access.req_seed_l01"
    if sid == 0x27 and sub == 0x02: return "sec_access.send_key_l01"
    if sid == 0x27 and sub == 0x0B: return "sec_access.req_seed_SAS"
    if sid == 0x27 and sub == 0x0C: return "sec_access.send_key_SAS"
    if sid == 0xAA: return "dynamic_did"
    if sid == 0xAE: return "response_on_event"
    if sid == 0x3E and sub == 0x80: return "tester_present_broadcast"
    if sid == 0x3D: return "write_memory"
    if sid == 0x23: return "read_memory_by_addr"
    if sid == 0x7F:
        bad_sid = uds[1] if len(uds) > 1 else 0
        return f"NRC.0x{bad_sid:02X}"
    if sid >= 0x40:
        return "+response"
    return f"sid_0x{sid:02X}"

def segment(timeline):
    """Group rows into 'phases' by run of the same step-type or by long time gap."""
    if not timeline: return []
    phases = []
    cur = None
    GAP_MS = 1500  # >1.5s gap = new phase
    for row in timeline:
        stype = detect_step_type(row)
        if row["dir"] == "RX":
            if cur: cur["rx"] += 1
            continue
        if cur is None:
            cur = {"step": stype, "t_start": row["t_ms"], "t_end": row["t_ms"],
                   "ecu_ids": set(), "tx": 0, "rx": 0, "samples": []}
        gap = row["t_ms"] - cur["t_end"]
        if stype != cur["step"] or gap > GAP_MS:
            # close current, start new
            cur["ecu_ids"] = sorted(cur["ecu_ids"])
            phases.append(cur)
            cur = {"step": stype, "t_start": row["t_ms"], "t_end": row["t_ms"],
                   "ecu_ids": set(), "tx": 0, "rx": 0, "samples": []}
        cur["tx"] += 1
        cur["t_end"] = row["t_ms"]
        cur["ecu_ids"].add(row["can_id"])
        if len(cur["samples"]) < 2:
            cur["samples"].append({"can_id": row["can_id"], "uds": row["uds_hex"], "decoded": row["uds_decoded"]})
    if cur:
        cur["ecu_ids"] = sorted(cur["ecu_ids"])
        phases.append(cur)
    return phases

if __name__ == "__main__":
    timeline = json.loads(Path(sys.argv[1]).read_text())
    phases = segment(timeline)
    for i, p in enumerate(phases):
        ecus = ",".join(p["ecu_ids"][:5])
        if len(p["ecu_ids"]) > 5: ecus += f",+{len(p['ecu_ids'])-5}"
        dur = p["t_end"] - p["t_start"]
        print(f"#{i:02d} t={p['t_start']:>7d}ms +{dur:>5d}ms  step={p['step']:<28}  tx={p['tx']:3d} rx={p['rx']:3d}  ecus=[{ecus}]")
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(json.dumps(phases, indent=2))
        print(f"\nwrote {len(phases)} phases → {sys.argv[2]}")
