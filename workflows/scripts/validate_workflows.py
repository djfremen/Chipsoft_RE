"""
Sanity-check every workflow definition.json against the source shim logs.
Verifies that every (request_can_id, uds) in `steps` actually appears in the
referenced capture(s), and warns on definitions that claim capture but the
log doesn't contain the expected bytes.
"""
import json, re, sys
from pathlib import Path

WORKFLOWS_DIR = Path(__file__).resolve().parent.parent
SHIM_RAW = WORKFLOWS_DIR.parent / "shim" / "cstech2win" / "captures" / "raw"

def all_uds_in(log_path: Path) -> set[str]:
    """Return set of '<can_id_hex>:<uds_hex>' actually present in the shim log."""
    s = set()
    pat = re.compile(r"\|REQ-PDU\|len=\d+\|([0-9A-Fa-f ]+)")
    for line in log_path.read_text(errors="ignore").splitlines():
        m = pat.search(line)
        if not m: continue
        bs = bytes.fromhex(m.group(1).replace(" ", ""))
        if len(bs) < 5: continue
        can = int.from_bytes(bs[:4], "big") & 0xFFFFFFFF
        s.add(f"0x{can:04X}:{bs[4:].hex(' ')}")
    return s

def check_workflow(wf_path: Path) -> list[str]:
    issues = []
    wf = json.loads(wf_path.read_text())
    name = wf.get("name", wf_path.parent.name)
    captures = wf.get("captured_from", [])
    if wf.get("status", "").startswith("DEFINITION_PENDING"):
        return [f"{name}: PENDING — skipped"]
    if not captures:
        return [f"{name}: WARN no captured_from"]
    # Resolve capture log paths
    found = set()
    for c in captures:
        p = Path(c)
        if not p.is_absolute():
            p = WORKFLOWS_DIR.parent.parent / c
        if p.exists():
            found |= all_uds_in(p)
        else:
            issues.append(f"{name}: missing capture {p}")
    # Spot-check a few steps that have concrete tx fields.
    # Keys stored as "0x0241:aa 01 01" (lowercase 0x prefix, lowercase hex bytes).
    def has(can_hex, uds_hex):
        can_key = can_hex.lower()
        if not can_key.startswith("0x"): can_key = "0x" + can_key
        # Normalize spacing on the UDS bytes too
        needle = uds_hex.lower().replace(" ", " ")
        return any(k.startswith(f"{can_key}:") and needle in k for k in found)
    for step in wf.get("steps", []):
        tx = step.get("tx")
        if tx and isinstance(tx.get("can_id"), str) and "${" not in tx["can_id"]:
            cid = tx["can_id"]
            uds = tx.get("uds", "")
            if not has(cid, uds):
                issues.append(f"{name}: step '{step.get('step')}' tx ({cid}, {uds}) not found in captures")
    if not issues:
        issues.append(f"{name}: OK")
    return issues

if __name__ == "__main__":
    out = []
    for d in sorted(WORKFLOWS_DIR.glob("*/*/definition.json")):
        out.extend(check_workflow(d))
    for line in out:
        print(line)
