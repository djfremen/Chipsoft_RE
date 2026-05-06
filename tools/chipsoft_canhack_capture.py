#!/usr/bin/env python3
"""
chipsoft_canhack_capture.py

Listen-only CAN sniffer for a Chipsoft Pro flashed with canhacker_pro.bin.
Writes a Vector ASC log (cross-tool compatible: CANHacker, SavvyCAN, Wireshark,
BUSMASTER) plus a raw SLCAN trace for archival.

Why a custom open path instead of `python-can`'s slcanBus:
    python-can's slcan interface hardcodes the open command to `O` (active).
    On a bench bus where the ECM is the only other node, an ACKing second
    adapter changes Tech2's behavior. We need the Lawicel `L` (listen-only)
    open instead — device never transmits, including ACKs. So we drive the
    serial port directly and use python-can purely as the ASC writer.

Usage:
    pip install pyserial python-can
    python chipsoft_canhack_capture.py COM7                  # SAAB SWCAN 33.3k
    python chipsoft_canhack_capture.py COM7 --speed S6       # HS-CAN 500k
    python chipsoft_canhack_capture.py COM7 --asc out.asc    # custom output path

Output (default names use a timestamp):
    capture-<ts>.asc     Vector ASC log
    capture-<ts>.slcan   raw Lawicel trace + init transcript
"""
import argparse
import datetime
import sys
import time

try:
    import serial
except ImportError:
    print("ERROR: pyserial not installed. Run: pip install pyserial", file=sys.stderr)
    sys.exit(2)

try:
    import can
    from can.io import ASCWriter
except ImportError:
    print("ERROR: python-can not installed. Run: pip install python-can", file=sys.stderr)
    sys.exit(2)


SPEED_PRESETS = {
    "S0": 10_000, "S1": 20_000, "S2": 50_000, "S3": 100_000, "S4": 125_000,
    "S5": 250_000, "S6": 500_000, "S7": 800_000, "S8": 1_000_000,
}


def now_iso() -> str:
    return datetime.datetime.now().isoformat(timespec="milliseconds")


def send(ser: serial.Serial, cmd: str, *, log) -> bytes:
    payload = (cmd + "\r").encode("ascii")
    ser.write(payload)
    log(f"[{now_iso()}] >> {cmd!r}")
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


def parse_lawicel_frame(line: str):
    """Parse a Lawicel frame line. Returns (arb_id, is_extended, data) or None."""
    if not line:
        return None
    tag = line[0]
    if tag == "t":  # 11-bit data
        if len(line) < 5:
            return None
        try:
            arb_id = int(line[1:4], 16)
            dlc = int(line[4])
        except ValueError:
            return None
        hex_data = line[5:5 + dlc * 2]
        if len(hex_data) != dlc * 2:
            return None
        try:
            return arb_id, False, bytes.fromhex(hex_data)
        except ValueError:
            return None
    if tag == "T":  # 29-bit data
        if len(line) < 10:
            return None
        try:
            arb_id = int(line[1:9], 16)
            dlc = int(line[9])
        except ValueError:
            return None
        hex_data = line[10:10 + dlc * 2]
        if len(hex_data) != dlc * 2:
            return None
        try:
            return arb_id, True, bytes.fromhex(hex_data)
        except ValueError:
            return None
    return None  # RTR / status / other tags ignored for now


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("port", help="COM port (e.g. COM7) or /dev/ttyUSB0")
    ap.add_argument("--baud", type=int, default=115200,
                    help="Host-side serial baud (Lawicel std: 115200)")
    ap.add_argument("--speed", default=None,
                    help="Lawicel preset: S0=10k S1=20k S2=50k S3=100k S4=125k "
                         "S5=250k S6=500k S7=800k S8=1M. Overrides --divisor.")
    ap.add_argument("--divisor", type=int, default=30,
                    help="User Def divisor (1_000_000/N). Default 30 = 33.333k SWCAN.")
    ap.add_argument("--raw-cmd", default=None,
                    help="Override the whole init with one raw lawicel command. "
                         "Example: 's003A'")
    ap.add_argument("--active", action="store_true",
                    help="Open in NORMAL/active mode (O) instead of listen-only (L). "
                         "Default is listen-only — never transmits or ACKs.")
    ap.add_argument("--asc", default=None,
                    help="Vector ASC output path. Default: capture-<ts>.asc")
    ap.add_argument("--slcan-log", default=None,
                    help="Raw SLCAN trace path. Default: capture-<ts>.slcan")
    args = ap.parse_args()

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    asc_path = args.asc or f"capture-{ts}.asc"
    slcan_path = args.slcan_log or f"capture-{ts}.slcan"

    print(f"opening port  : {args.port} @ {args.baud}", flush=True)
    print(f"asc log       : {asc_path}", flush=True)
    print(f"slcan trace   : {slcan_path}", flush=True)

    ser = serial.Serial(
        args.port, args.baud,
        bytesize=8, parity="N", stopbits=1,
        timeout=0.05, write_timeout=1.0,
    )

    slcan_f = open(slcan_path, "w", buffering=1)
    def log(line: str):
        print(line, flush=True)
        slcan_f.write(line + "\n")

    log(f"# chipsoft_canhack_capture started {now_iso()}")
    log(f"# port={args.port} baud={args.baud}")

    # 1. Close any prior session
    send(ser, "C", log=log)

    # 2. Set bit rate (preset, divisor, or raw override)
    configured_bitrate = None
    if args.raw_cmd:
        send(ser, args.raw_cmd, log=log)
    elif args.speed:
        if args.speed not in SPEED_PRESETS:
            print("--speed must be one of S0..S8", file=sys.stderr)
            return 2
        send(ser, args.speed, log=log)
        configured_bitrate = SPEED_PRESETS[args.speed]
    else:
        configured_bitrate = 1_000_000 // args.divisor
        r1 = send(ser, f"d{args.divisor}", log=log)
        if r1.endswith(b"\x07"):
            log("# 'd' divisor rejected; trying 's<N>'")
            r2 = send(ser, f"s{args.divisor:04X}", log=log)
            if r2.endswith(b"\x07"):
                log("# both divisor forms rejected — try --raw-cmd or --speed S?")

    # 3. Open channel — listen-only by default
    open_cmd = "O" if args.active else "L"
    send(ser, open_cmd, log=log)

    mode = "ACTIVE" if args.active else "LISTEN-ONLY"
    log(f"# capture begins  mode={mode}  bitrate={configured_bitrate}")
    log(f"# Ctrl-C to stop\n")

    asc_writer = ASCWriter(asc_path)
    line = bytearray()
    frame_count = 0
    parse_errors = 0

    try:
        while True:
            b = ser.read(1)
            if not b:
                continue
            line += b
            if b == b"\r":
                txt = bytes(line[:-1]).decode("ascii", errors="replace")
                line.clear()
                if not txt:
                    continue
                log(f"[{now_iso()}] {txt}")
                parsed = parse_lawicel_frame(txt)
                if parsed is None:
                    if txt[0] in ("t", "T"):
                        parse_errors += 1
                    continue
                arb_id, is_ext, data = parsed
                msg = can.Message(
                    timestamp=time.time(),
                    arbitration_id=arb_id,
                    is_extended_id=is_ext,
                    data=data,
                )
                asc_writer.on_message_received(msg)
                frame_count += 1
            elif b == b"\x07":
                log(f"[{now_iso()}] <BEL: device error>")
                line.clear()
    except KeyboardInterrupt:
        log(f"\n# Ctrl-C — {frame_count} frames captured, {parse_errors} parse errors")
    finally:
        try:
            ser.write(b"C\r")
        except Exception:
            pass
        ser.close()
        asc_writer.stop()
        slcan_f.close()

    print(f"\n.asc saved to    {asc_path}", flush=True)
    print(f".slcan saved to  {slcan_path}", flush=True)
    print(f"frames captured  {frame_count}", flush=True)
    if parse_errors:
        print(f"parse errors     {parse_errors}  (frames in raw .slcan trace only)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
