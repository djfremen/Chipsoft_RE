# Workflow Catalogue Index

| Workflow | Vehicle | Status | Notes |
|---|---|---|---|
| [saab/module_presence_scan](saab/module_presence_scan/definition.json) | SAAB GMLAN | ✅ captured | $1A 9A broadcast on 0x0101 |
| [saab/vin_read](saab/vin_read/definition.json) | SAAB | ✅ captured | $1A 90 on 0x0241 or 0x07E0 |
| [saab/seed_sweep_l01](saab/seed_sweep_l01/definition.json) | SAAB | ✅ captured (10 of 12 ECMs) | $27 01 across 12 CAN-IDs; slots 5/6 source unknown |
| [saab/engine_sas_unlock](saab/engine_sas_unlock/definition.json) | SAAB engine | ⚠️ partial | seed step captured (0xC4DC); $27 0C ack pending |
| [saab/engine_ssa_writeback](saab/engine_ssa_writeback/definition.json) | SAAB engine | ❌ pending | $3D write of 714B; needs bench capture |
| [saab/check_ignition_key_status](saab/check_ignition_key_status/definition.json) | SAAB engine | ✅ captured | $AE 03 02 + DPID 0x0B; bit layout TBD |

## Source captures referenced

- `cstech2win_shim_20260507-015619.log` — primary, 146 req+rsp rows
- `cstech2win_shim_20260507-175608.log` — 178 rows, broader sweep
- `cstech2win_shim_20260507-014723.log` — 130 rows
- `cstech2win_shim_20260513-113205.log` — 2026-05-13 check ignition key status, 51 rows

## How to consume

Each `definition.json` is portable across hosts. A server-side workflow engine
(Python/Node/Go) walks `steps[]`, calls a `chipsoft.tx(can_id, uds)` shim per
step, parses replies, fills `session_var.*`, and feeds the next step.

The client (Android/WebUSB/etc.) doesn't read these JSON files. It only relays
USB bytes. All workflow logic stays server-side.
