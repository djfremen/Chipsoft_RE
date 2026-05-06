#!/usr/bin/env python3
"""
SLCAN capture for Chipsoft Pro in CANHacker mode.

What this does:
- Opens the device's virtual COM port at 115200 baud.
- Issues lawicel-style init: close any prior session, set bit rate (default 33.3k
  for SAAB SWCAN), open in LISTEN-ONLY mode.
- Tails the port, prints every received line to stdout, writes timestamped
  lines to a log file.

Why listen-only: on a bench bus where the ECM is the only other node, an
ACKing second adapter changes Tech2's behavior. `L\r` opens listen-only;
the device never transmits, including ACKs.

Usage:
  pip install pyserial
  python slcan_capture.py COM7                        # default = 33.3k SWCAN
  python slcan_capture.py COM7 --speed S6             # 500k HSCAN preset
  python slcan_capture.py COM7 --raw-cmd "s003A"      # custom BTR (try if -d fails)

Bit-rate handling for the Chipsoft:
  The vendor manual documents User Def speed via a divisor (1_000_000 / N).
  divisor 30 -> 33.333 kbps (SAAB SWCAN).
  Wire-level SLCAN syntax for setting that divisor is undocumented; we try
  in this order:
    1. Standard lawicel preset (e.g. S6) if --speed S? was given
    2. Divisor command   `d<N>\r`     (most likely Chipsoft form)
    3. Lower-case S      `s<N>\r`     (some vendors use this for divisor)
  If none of those work, pass --raw-cmd to override the entire init.

Ctrl-C exits cleanly and the device closes the channel.
"""
import argparse
import datetime
import os
import sys
import time

try:
    import serial
except ImportError:
    print("ERROR: pyserial not installed.  Run:  pip install pyserial", file=sys.stderr)
    sys.exit(2)


def now_iso() -> str:
    return datetime.datetime.now().isoformat(timespec="milliseconds")


def send(ser: serial.Serial, cmd: str, *, log) -> bytes:
    """Write a lawicel command (auto-appends \\r) and read one bell/CR-terminated response."""
    payload = (cmd + "\r").encode("ascii")
    ser.write(payload)
    log(f"[{now_iso()}] >> {cmd!r}")
    # Read until \r (0x0D) or BEL (0x07).  Up to 256 bytes.
    buf = bytearray()
    deadline = time.time() + 1.0
    while time.time() < deadline:
        b = ser.read(1)
        if not b:
            continue
        buf += b
        if b in (b"\r", b"\x07"):
            break
    log(f"[{now_iso()}] << {bytes(buf)!r}")
    return bytes(buf)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("port", help="COM port (e.g. COM7) or /dev/ttyUSB0")
    ap.add_argument("--baud", type=int, default=115200,
                    help="Host-side serial baud (default 115200; lawicel std)")
    ap.add_argument("--speed", default=None,
                    help="Lawicel preset bit rate: S0=10k S1=20k S2=50k S3=100k S4=125k S5=250k S6=500k S7=800k S8=1M")
    ap.add_argument("--divisor", type=int, default=30,
                    help="User Def divisor (1_000_000/N).  Default 30 = 33.333 kbps for SAAB SWCAN.  Ignored if --speed set.")
    ap.add_argument("--raw-cmd", default=None,
                    help="Override the whole init sequence with a single raw lawicel command (no leading 'O'/'L'/'C'). Example: 's003A'")
    ap.add_argument("--active", action="store_true",
                    help="Open in NORMAL/active mode (O) instead of listen-only (L). Default is listen-only — safer.")
    ap.add_argument("--log", default=None,
                    help="Log file path. Default: capture-YYYYMMDD-HHMMSS.slcan")
    args = ap.parse_args()

    log_path = args.log or f"capture-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.slcan"
    print(f"opening port  : {args.port} @ {args.baud}", flush=True)
    print(f"log file      : {log_path}", flush=True)

    ser = serial.Serial(
        args.port, args.baud,
        bytesize=8, parity="N", stopbits=1,
        timeout=0.05, write_timeout=1.0,
    )

    log_f = open(log_path, "w", buffering=1)
    def log(line: str):
        print(line, flush=True)
        log_f.write(line + "\n")

    log(f"# slcan_capture started {now_iso()}  port={args.port}  baud={args.baud}")

    # 1. Close any prior session
    send(ser, "C", log=log)

    # 2. Set bit rate.  Try in order: preset (if given) -> divisor 'd' -> divisor 's'.
    if args.raw_cmd:
        send(ser, args.raw_cmd, log=log)
    elif args.speed:
        if not args.speed.startswith("S") or args.speed not in {f"S{i}" for i in range(9)}:
            print("--speed must be S0..S8", file=sys.stderr)
            return 2
        send(ser, args.speed, log=log)
    else:
        # Try divisor commands; the device should bell-reject the wrong one.
        r1 = send(ser, f"d{args.divisor}", log=log)
        if r1.endswith(b"\x07"):  # BEL = error
            log("# 'd' divisor cmd rejected; trying 's<N>'")
            r2 = send(ser, f"s{args.divisor:04X}", log=log)
            if r2.endswith(b"\x07"):
                log("# both divisor forms rejected — try --raw-cmd or --speed S?")

    # 3. Open the channel
    open_cmd = "O" if args.active else "L"
    send(ser, open_cmd, log=log)

    # 4. Read loop — tail every line received, timestamp it
    log(f"# capture begins  open_mode={'ACTIVE' if args.active else 'LISTEN-ONLY'}")
    log(f"# CAN frames format:  t<id3hex><len><data>  (11-bit)")
    log(f"# CAN frames format:  T<id8hex><len><data>  (29-bit)")
    log(f"# Ctrl-C to stop\n")

    line = bytearray()
    try:
        while True:
            b = ser.read(1)
            if not b:
                continue
            line += b
            if b == b"\r":
                # got a complete line
                txt = line[:-1].decode("ascii", errors="replace")
                if txt:  # skip empty
                    log(f"[{now_iso()}] {txt}")
                line.clear()
            elif b == b"\x07":
                log(f"[{now_iso()}] <BEL: device error>")
                line.clear()
    except KeyboardInterrupt:
        log(f"\n# Ctrl-C — closing channel")
    finally:
        try:
            ser.write(b"C\r")
        except Exception:
            pass
        ser.close()
        log_f.close()

    print(f"\nlog saved to {log_path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
