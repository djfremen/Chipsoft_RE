# OpenClaw Workflow Catalogue

This directory catalogues **diagnostic workflows** extracted from real Tech2Win
shim captures, in a form portable to any host (Android, browser, server API).

## Layout

```
workflows/
├── README.md                       <- this file
├── INDEX.md                        <- machine-readable index of all workflows
├── scripts/                        <- parser + segmenter + validators
├── captured/                       <- raw timelines + phases from shim logs
└── <vehicle>/<workflow_name>/
    ├── definition.json             <- abstract workflow steps
    ├── README.md                   <- human description + provenance
    └── captures/                   <- copies of the source shim logs
```

## Workflow definition shape

```json
{
  "name": "<vehicle>/<workflow_name>",
  "vehicle": "SAAB 9-3 / 9-5 (GMLAN)",
  "purpose": "...",
  "captured_from": ["<shim_log_path>"],
  "steps": [
    {
      "step": "step-name",
      "tx": {"can_id": "0x0241", "uds": "10 02"},
      "expect": {"sid": "0x50", "sub": "0x02"},
      "timeout_ms": 500,
      "on_pending": "wait_and_repoll",
      "max_retries": 3
    },
    ...
  ]
}
```

## Status (2026-05-11)

- ✅ `saab/module_presence_scan` — 12-ECM `$1A 9A` probe
- ✅ `saab/vin_read` — `$1A 90` at `$0241` and OBD-II `$07E0`
- ✅ `saab/seed_sweep_l01` — `$27 01` across 9-12 ECMs (builds the pre-auth SKA tuples)
- ⚠️  `saab/engine_sas_unlock` — `$10 02 → $27 0B → seed → $27 0C → ack`; we have through the seed step (seed `0xC4DC`), missing the key-send + ack because SAS server was unreachable in the 2026-05-07 captures
- ❌ `saab/engine_ssa_writeback` — `$3D` write of post-auth to SSA region; no capture yet

To fill the gaps, one bench session with shim active end-to-end is needed.

## Source data

- Parser: `scripts/parse_shim_to_timeline.py` — `.log → timeline.json`
- Segmenter: `scripts/segment_workflow.py` — `timeline.json → phases.json`
- Original shim logs: `../shim/cstech2win/captures/raw/`
