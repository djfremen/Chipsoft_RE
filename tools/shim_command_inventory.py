#!/usr/bin/env python3
"""Decipher every captured CSTech2Win shim log with scapy and emit a
canonical command inventory.

Walks every ``*.log`` under the captures directory, runs each REQ-PDU /
RSP-UDS line through scapy's GMLAN dissector, and groups the results by
ECU address pair, service, and NRC. Outputs Markdown (for humans) and
JSON (for the workflow extractor).

Outputs land under ``Chipsoft_RE/notes/`` with today's date.

Usage:
    python3 shim_command_inventory.py            # all captures
    python3 shim_command_inventory.py --src LOG  # one log
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

logging.getLogger("scapy").setLevel(logging.ERROR)

from scapy.contrib.automotive.gm.gmlan import GMLAN  # noqa: E402
from scapy.config import conf  # noqa: E402

conf.contribs['GMLAN'] = {
    'treat-response-pending-as-answer': True,
    'single_layer_mode': False,
    'compatibility_mode': True,
}

LINE_RE = re.compile(
    r"^(?P<ms>\d+)\|(?P<tid>\d+)\|HEX\s*\|"
    r"(?P<kind>REQ-PDU|RSP-UDS)\|len=(?P<len>\d+)\|(?P<hex>.+)$"
)

CAPTURES_DIR = Path(__file__).resolve().parent.parent / "shim/cstech2win/captures"

# Scapy GMLAN service-ID map (request side); used to label unknown SIDs.
GMLAN_SERVICE_NAMES = {
    0x04: "ClearDiagnosticInformation",
    0x10: "InitiateDiagnosticOperation",
    0x12: "ReadFailureRecordData",
    0x1A: "ReadDataByIdentifier",
    0x20: "ReturnToNormalOperation",
    0x22: "ReadDataByParameterIdentifier",
    0x23: "ReadMemoryByAddress",
    0x27: "SecurityAccess",
    0x28: "DisableNormalCommunication",
    0x2C: "DefineDPID",
    0x2D: "DefinePIDByAddress",
    0x34: "RequestDownload",
    0x36: "TransferData",
    0x3B: "WriteDataByIdentifier",
    0x3E: "TesterPresent",
    0x7F: "NegativeResponse",
    0xA2: "ReportProgrammingState",
    0xA5: "ProgrammingMode",
    0xA9: "ReadDiagnosticInformation",
    0xAA: "ReadDataByPacketIdentifier",
    0xAE: "DeviceControl",
    0xFE: "SAAB_FunctionalBroadcastPrefix",   # SAAB-specific, scapy unaware
}
# Positive-response = request SID + 0x40 (UDS convention)
GMLAN_RESPONSE_NAMES = {sid + 0x40: name + "PositiveResponse"
                        for sid, name in GMLAN_SERVICE_NAMES.items()
                        if sid != 0x7F}

NRC_NAMES = {
    0x10: "generalReject",
    0x11: "serviceNotSupported",
    0x12: "subFunctionNotSupported",
    0x21: "busyRepeatRequest",
    0x22: "conditionsNotCorrect",
    0x31: "requestOutOfRange",
    0x33: "securityAccessDenied",
    0x35: "invalidKey",
    0x36: "exceededNumberOfAttempts",
    0x37: "requiredTimeDelayNotExpired",
    0x78: "responsePending",
    0x7E: "subFunctionNotSupportedInActiveSession",
    0x7F: "serviceNotSupportedInActiveSession",
}

# Known GMLAN 11-bit address pairs from Jason Gaunt 2013 / SAAB observations.
ECU_NAMES = {
    0x0100: "InitialWakeUpRequest",
    0x0101: "RequestToAllNodes(broadcast)",
    0x0102: "DiagnosticRequest",
    0x0240: "ToReservedRequest",
    0x0241: "BCM/EngineDiag(SAAB)",
    0x0242: "TDM",
    0x0243: "EBCM",
    0x0244: "EHU",
    0x0245: "ECU_0x0245",
    0x0246: "SIC",
    0x0247: "SDC",
    0x0248: "ECU_0x0248",
    0x024A: "ECU_0x024A",
    0x024B: "ECU_0x024B",
    0x024C: "IPC",
    0x0251: "HVAC",
    0x0257: "ECU_0x0257",
    0x0258: "RFA",
    0x0540: "SF_FromReservedResponse",
    0x0541: "SF_From_0x0541",
    0x0641: "MF_FromBCM(SAAB engine reply)",
    0x0642: "MF_FromTDM",
    0x0643: "MF_FromEBCM",
    0x0644: "MF_FromEHU",
    0x0645: "MF_From_0x0645",
    0x0646: "MF_FromSIC",
    0x0647: "MF_FromSDC",
    0x0648: "MF_From_0x0648",
    0x0649: "MF_From_0x0649",
    0x064A: "MF_From_0x064A",
    0x064B: "MF_From_0x064B",
    0x064C: "MF_FromIPC",
    0x064D: "MF_From_0x064D",
    0x064F: "MF_From_0x064F",
    0x0651: "MF_FromHVAC",
    0x0657: "MF_From_0x0657",
    0x0658: "MF_FromRFA",
    0x065B: "MF_From_0x065B",
    0x065C: "MF_From_0x065C",
    0x07DF: "OBD_FunctionalRequest",
    0x07E0: "OBD_ToECM",
    0x07E1: "OBD_ToTCM",
    0x07E8: "OBD_FromECM",
    0x07E9: "OBD_FromTCM",
}


@dataclass
class Frame:
    log: str
    ms: int
    direction: str
    can_id: int
    uds_bytes: bytes


@dataclass
class ServiceStat:
    name: str
    count: int = 0
    example_payloads: list[str] = field(default_factory=list)

    def record(self, payload_hex: str) -> None:
        self.count += 1
        if len(self.example_payloads) < 3 and payload_hex not in self.example_payloads:
            self.example_payloads.append(payload_hex)


def _parse_line(log_name: str, line: str) -> Optional[Frame]:
    m = LINE_RE.match(line)
    if not m:
        return None
    try:
        raw = bytes.fromhex(m.group("hex").replace(" ", ""))
    except ValueError:
        return None
    if len(raw) < 5:
        return None
    can_id = (raw[2] << 8) | raw[3]
    uds = raw[4:]
    direction = "TX" if m.group("kind") == "REQ-PDU" else "RX"
    return Frame(log_name, int(m.group("ms")), direction, can_id, uds)


def _classify(uds: bytes) -> tuple[int, Optional[int], Optional[int], str]:
    """Return (sid, sub, nrc, label)."""
    if not uds:
        return (0, None, None, "<empty>")
    sid = uds[0]
    sub: Optional[int] = uds[1] if len(uds) >= 2 else None
    nrc: Optional[int] = None
    if sid == 0x7F and len(uds) >= 3:
        # 7F <requested_sid> <nrc>
        nrc = uds[2]
        rq_sid = uds[1]
        rq_name = GMLAN_SERVICE_NAMES.get(rq_sid, f"SID_0x{rq_sid:02X}")
        nrc_name = NRC_NAMES.get(nrc, f"NRC_0x{nrc:02X}")
        return (sid, rq_sid, nrc, f"NegativeResponse({rq_name}, {nrc_name})")
    # Positive response or request
    name = (GMLAN_RESPONSE_NAMES.get(sid)
            or GMLAN_SERVICE_NAMES.get(sid)
            or f"SID_0x{sid:02X}")
    return (sid, sub, None, name)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", help="single log path to process")
    ap.add_argument("--out", default=None,
                    help="output base path (default: notes/<date>-command-inventory)")
    args = ap.parse_args()

    if args.src:
        log_paths = [Path(args.src)]
    else:
        log_paths = sorted(CAPTURES_DIR.glob("*.log"))
    if not log_paths:
        sys.exit(f"no logs found under {CAPTURES_DIR}")

    # frames_by_ecu_pair[(tx_can, rx_can)] = list of frames
    frames: list[Frame] = []
    by_log: Counter[str] = Counter()
    for path in log_paths:
        for line in path.read_text(errors="replace").splitlines():
            f = _parse_line(path.name, line)
            if f is None:
                continue
            frames.append(f)
            by_log[path.name] += 1

    # Per ECU (TX direction), what services were sent. Per RX address, what
    # services were received. NRC tally.
    tx_services: dict[int, dict[str, ServiceStat]] = defaultdict(dict)
    rx_services: dict[int, dict[str, ServiceStat]] = defaultdict(dict)
    nrc_by_sid: dict[int, Counter[int]] = defaultdict(Counter)
    all_sids_tx: Counter[int] = Counter()
    all_sids_rx: Counter[int] = Counter()
    addresses_tx: Counter[int] = Counter()
    addresses_rx: Counter[int] = Counter()

    for f in frames:
        sid, sub, nrc, label = _classify(f.uds_bytes)
        bucket = tx_services if f.direction == "TX" else rx_services
        addr_counter = addresses_tx if f.direction == "TX" else addresses_rx
        addr_counter[f.can_id] += 1
        stats = bucket[f.can_id].setdefault(label, ServiceStat(label))
        stats.record(f.uds_bytes.hex(" "))
        if f.direction == "TX":
            all_sids_tx[sid] += 1
        else:
            all_sids_rx[sid] += 1
        if nrc is not None and sub is not None:
            nrc_by_sid[sub][nrc] += 1

    # Build the markdown report.
    md = [
        "# CSTech2Win shim command inventory",
        f"_Generated 2026-05-12 from {len(log_paths)} shim logs._",
        "",
        "## Logs ingested",
        "",
        "| Log | Frames |",
        "|---|---|",
    ]
    for log_name, n in by_log.most_common():
        md.append(f"| `{log_name}` | {n} |")
    md.append("")

    md.append("## Address summary")
    md.append("")
    md.append("### TX addresses (Tech2 → bus)")
    md.append("")
    md.append("| CAN ID | Label | Frame count |")
    md.append("|---|---|---|")
    for addr, n in addresses_tx.most_common():
        name = ECU_NAMES.get(addr, "unknown")
        md.append(f"| `${addr:04X}` | {name} | {n} |")
    md.append("")
    md.append("### RX addresses (bus → Tech2)")
    md.append("")
    md.append("| CAN ID | Label | Frame count |")
    md.append("|---|---|---|")
    for addr, n in addresses_rx.most_common():
        name = ECU_NAMES.get(addr, "unknown")
        md.append(f"| `${addr:04X}` | {name} | {n} |")
    md.append("")

    md.append("## Service inventory by ECU (TX)")
    md.append("")
    for addr in sorted(tx_services.keys()):
        name = ECU_NAMES.get(addr, "unknown")
        md.append(f"### `${addr:04X}` — {name}")
        md.append("")
        md.append("| Service | Count | Example payloads |")
        md.append("|---|---|---|")
        for label, stat in sorted(tx_services[addr].items(),
                                  key=lambda kv: -kv[1].count):
            examples = "<br>".join(f"`{p}`" for p in stat.example_payloads)
            md.append(f"| {stat.name} | {stat.count} | {examples} |")
        md.append("")

    md.append("## Response inventory by ECU (RX)")
    md.append("")
    for addr in sorted(rx_services.keys()):
        name = ECU_NAMES.get(addr, "unknown")
        md.append(f"### `${addr:04X}` — {name}")
        md.append("")
        md.append("| Service | Count | Example payloads |")
        md.append("|---|---|---|")
        for label, stat in sorted(rx_services[addr].items(),
                                  key=lambda kv: -kv[1].count):
            examples = "<br>".join(f"`{p}`" for p in stat.example_payloads)
            md.append(f"| {stat.name} | {stat.count} | {examples} |")
        md.append("")

    md.append("## Negative-response code distribution")
    md.append("")
    md.append("| Requested SID | NRC | Name | Count |")
    md.append("|---|---|---|---|")
    for rq_sid in sorted(nrc_by_sid.keys()):
        rq_name = GMLAN_SERVICE_NAMES.get(rq_sid, f"SID_0x{rq_sid:02X}")
        for nrc, n in nrc_by_sid[rq_sid].most_common():
            nrc_name = NRC_NAMES.get(nrc, f"NRC_0x{nrc:02X}")
            md.append(f"| `0x{rq_sid:02X}` ({rq_name}) | `0x{nrc:02X}` | {nrc_name} | {n} |")
    md.append("")

    md.append("## Top SIDs (TX)")
    md.append("")
    md.append("| SID | Service | Count |")
    md.append("|---|---|---|")
    for sid, n in all_sids_tx.most_common():
        name = GMLAN_SERVICE_NAMES.get(sid, f"SID_0x{sid:02X}")
        md.append(f"| `0x{sid:02X}` | {name} | {n} |")
    md.append("")

    md.append("## Top SIDs (RX)")
    md.append("")
    md.append("| SID | Service | Count |")
    md.append("|---|---|---|")
    for sid, n in all_sids_rx.most_common():
        # RX is mostly positive responses (sid = req_sid + 0x40)
        name = GMLAN_RESPONSE_NAMES.get(sid) or GMLAN_SERVICE_NAMES.get(sid) or f"SID_0x{sid:02X}"
        md.append(f"| `0x{sid:02X}` | {name} | {n} |")
    md.append("")

    # JSON sibling
    js = {
        "generated": str(date.today()),
        "logs": dict(by_log),
        "addresses_tx": {f"0x{k:04X}": v for k, v in addresses_tx.items()},
        "addresses_rx": {f"0x{k:04X}": v for k, v in addresses_rx.items()},
        "tx_services": {
            f"0x{addr:04X}": {
                label: {"count": s.count, "examples": s.example_payloads}
                for label, s in svc.items()
            } for addr, svc in tx_services.items()
        },
        "rx_services": {
            f"0x{addr:04X}": {
                label: {"count": s.count, "examples": s.example_payloads}
                for label, s in svc.items()
            } for addr, svc in rx_services.items()
        },
        "nrc_by_sid": {f"0x{sid:02X}": {f"0x{nrc:02X}": n for nrc, n in c.items()}
                       for sid, c in nrc_by_sid.items()},
        "sid_totals_tx": {f"0x{sid:02X}": n for sid, n in all_sids_tx.items()},
        "sid_totals_rx": {f"0x{sid:02X}": n for sid, n in all_sids_rx.items()},
    }

    out_base = (Path(args.out) if args.out else
                Path(__file__).resolve().parent.parent /
                "notes" / f"{date.today()}-command-inventory")
    out_md = out_base.with_suffix(".md")
    out_json = out_base.with_suffix(".json")
    out_md.write_text("\n".join(md))
    out_json.write_text(json.dumps(js, indent=2))

    print(f"wrote {out_md}")
    print(f"wrote {out_json}")
    print()
    print(f"Total frames: {sum(by_log.values())}")
    print(f"Unique TX addresses: {len(addresses_tx)}")
    print(f"Unique RX addresses: {len(addresses_rx)}")
    print(f"Distinct request SIDs: {len(all_sids_tx)}")
    print(f"Distinct response SIDs: {len(all_sids_rx)}")


if __name__ == "__main__":
    main()
