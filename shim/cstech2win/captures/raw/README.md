# Raw shim logs

Unfiltered archive of every `cstech2win_shim_*.log` the shim has produced on Chris's bench machine, copied from `%TEMP%` and committed verbatim. Filenames are the shim's original timestamp format: `cstech2win_shim_YYYYMMDD-HHMMSS.log`. Sorted lexicographically = sorted by wall-clock time.

## Why this dir exists separately from the curated captures

The files at the root of `../captures/` are *curated* — handpicked logs renamed to `YYYY-MM-DD-shim-vN-<theme>.log` and paired with a sibling `.md` analysis. Each one represents a deliberate run an agent walked through line-by-line.

This `raw/` dir is the unfiltered version. Most of the small files (~500 bytes) are startup probes — Tech2Win loads, the shim attaches, Tech2Win immediately exits. They contain only the `DLL_PROCESS_ATTACH` and a couple of `PDUConstruct` calls, no useful capture. They're kept in case future agents want to verify behavior across attach cycles or look for crashes during init. The big files (>100 KB) are real Tech2Win sessions where the operator drove the SecurityAccess flow.

## Conventions

- **Don't rename files in this dir.** If you want a curated copy, also drop a renamed copy + analysis at `../captures/2026-MM-DD-shim-vN-<theme>.{log,md}`. Leave the raw file alone.
- **New raw logs are append-only.** When the bench machine produces new logs, copy the new ones in here, don't replace existing ones.
- **Match shim version → capture log via wall-clock time.** Cross-reference the timestamp in the filename against `git log shim/cstech2win/build/CSTech2Win.dll` to figure out which shim build produced which log. Each rebuilt shim binary's `mtime` brackets a window of logs.

## Quick inventory shortcuts

```bash
# List by size (largest = real sessions):
ls -laS shim/cstech2win/captures/raw/

# Find logs that captured a $27 0B request:
grep -l "27 0B" shim/cstech2win/captures/raw/*.log

# Find logs where Tech2 actually got a seed back:
grep -l "67 0B" shim/cstech2win/captures/raw/*.log

# Find logs with the canonical-struct RSP-UDS lines (v5+):
grep -l "RSP-UDS" shim/cstech2win/captures/raw/*.log
```

## Known mappings (raw → curated)

These curated logs in `../captures/` are byte-equal copies of these raw files (selected and renamed when the analysis was written):

| Curated | Raw source |
|---|---|
| `2026-05-06-shim-v1-first-run.log` | (one of the 2026-05-06 evening logs — see git blame) |
| `2026-05-07-shim-v4-rsp-payload.log` | `cstech2win_shim_20260507-000434.log` (best fit by size + content) |
| `2026-05-07-shim-v5-canonical-struct.log` | `cstech2win_shim_20260507-014723.log` (first run with `RSP-UDS`) |
| `2026-05-07-shim-v6-seed-deterministic.log` | `cstech2win_shim_20260507-015619.log` (second `0xC4DC` capture) |

Mappings are by best inference, not authoritative — if exact provenance matters, diff the byte content.
