#!/usr/bin/env python3
"""Auto-following live shim-log tail.

Polls the EliteBook over SSH every few seconds for the freshest
``cstech2win_shim_*.log`` and streams it through ``shim_log_decode.py``
into a Mac-side file. When Tech2Win restarts (new shim log spawns), the
wrapper detects the change and re-points the stream automatically.

Usage:
    python3 live_shim_tail.py
        --host elitebook@192.168.4.59
        --out  /tmp/saab_live_decode.log
        --poll 5
"""
from __future__ import annotations

import argparse
import os
import shlex
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
DECODER = HERE / "shim_log_decode.py"


def latest_log_path(host: str, timeout: int = 8) -> str | None:
    cmd = [
        "ssh", "-o", f"ConnectTimeout={timeout}", "-o", "BatchMode=yes", host,
        'powershell -NoProfile -Command "Get-ChildItem $env:TEMP -Filter '
        "'cstech2win_shim_*.log'"
        " | Sort-Object LastWriteTime -Descending"
        ' | Select-Object -First 1 -ExpandProperty FullName"',
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 2)
    except subprocess.TimeoutExpired:
        return None
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def start_pipeline(host: str, log_path: str, out_path: str,
                   decoder_python: str) -> subprocess.Popen:
    """Start ssh-tail | decoder >> out, return the ssh subprocess.

    The decoder is fed via pipe; closing the ssh process drains it cleanly.
    Output is appended (not truncated) so cross-session history stays in
    one place.
    """
    out_fh = open(out_path, "ab", buffering=0)
    ssh_cmd = [
        "ssh", "-o", "ServerAliveInterval=15", host,
        f'powershell -NoProfile -Command "Get-Content -Wait \'{log_path}\'"',
    ]
    # Annotate the switch so it's obvious in the decoded stream where a
    # new Tech2Win session starts.
    banner = f"\n=== session start {datetime.now():%H:%M:%S}  {log_path}\n"
    out_fh.write(banner.encode())
    out_fh.flush()

    ssh_proc = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL,
                                 preexec_fn=os.setsid)
    decoder_proc = subprocess.Popen(
        [decoder_python, str(DECODER), "-", "--no-color"],
        stdin=ssh_proc.stdout, stdout=out_fh, stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid,
    )
    # Close our copy so the decoder gets EOF when ssh ends.
    ssh_proc.stdout.close()
    ssh_proc._decoder = decoder_proc  # type: ignore[attr-defined]
    return ssh_proc


def stop_pipeline(proc: subprocess.Popen) -> None:
    for p in (proc, getattr(proc, "_decoder", None)):
        if p is None:
            continue
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="elitebook@192.168.4.59")
    ap.add_argument("--out", default="/tmp/saab_live_decode.log")
    ap.add_argument("--poll", type=float, default=5.0,
                    help="seconds between latest-log discovery polls")
    ap.add_argument("--python",
                    default=os.environ.get("DECODER_PYTHON", sys.executable),
                    help="python interpreter for the decoder (needs scapy)")
    args = ap.parse_args()

    current_path: str | None = None
    pipeline: subprocess.Popen | None = None
    last_status_t = 0.0

    def log(msg: str) -> None:
        print(f"[{datetime.now():%H:%M:%S}] {msg}", file=sys.stderr, flush=True)

    log(f"watching {args.host} for newest shim log every {args.poll}s; "
        f"decoded → {args.out}")

    try:
        while True:
            latest = latest_log_path(args.host)
            now = time.time()

            if latest is None:
                # SSH timed out or no logs yet. If we had a pipeline, leave
                # it running — the network blip might recover.
                if now - last_status_t > 30:
                    log(f"(no log found / ssh unreachable)")
                    last_status_t = now
            elif latest != current_path:
                if pipeline is not None:
                    log(f"switching shim log -> {Path(latest).name}")
                    stop_pipeline(pipeline)
                else:
                    log(f"following {Path(latest).name}")
                pipeline = start_pipeline(args.host, latest, args.out, args.python)
                current_path = latest
                last_status_t = now
            else:
                # No change. Print a periodic heartbeat so the operator
                # knows we're alive.
                if now - last_status_t > 60:
                    sz = Path(args.out).stat().st_size if Path(args.out).exists() else 0
                    log(f"still following {Path(latest).name}; decoded={sz} bytes")
                    last_status_t = now

            time.sleep(args.poll)
    except KeyboardInterrupt:
        log("shutting down")
    finally:
        if pipeline is not None:
            stop_pipeline(pipeline)


if __name__ == "__main__":
    main()
