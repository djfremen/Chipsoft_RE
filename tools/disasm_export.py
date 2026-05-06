#!/usr/bin/env python3
"""Disassemble a named export (or RVA) of a PE32 DLL using Capstone.

Usage:
  disasm_export.py <pe> <export-name>           # disassemble named export
  disasm_export.py <pe> 0x<rva> [--bytes N]     # disassemble at RVA
  disasm_export.py <pe> --list                  # list exports

Stops at the first ret-like instruction (ret/retn/retf) by default;
pass --bytes N to force a fixed window.
"""
import sys
from pathlib import Path
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_MODE_64

STOP_MNEMONICS = {"ret", "retn", "retf", "iret"}


def find_export(pe: pefile.PE, name: str):
    if not hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
        return None
    for sym in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if sym.name and sym.name.decode("latin-1") == name:
            return sym.address
    return None


def section_for_rva(pe: pefile.PE, rva: int):
    for s in pe.sections:
        start = s.VirtualAddress
        end = start + max(s.Misc_VirtualSize, s.SizeOfRawData)
        if start <= rva < end:
            return s
    return None


def read_bytes(pe: pefile.PE, rva: int, length: int) -> bytes:
    return pe.get_memory_mapped_image()[rva:rva + length]


def disasm(pe: pefile.PE, rva: int, max_bytes: int, stop_at_ret: bool):
    md = Cs(CS_ARCH_X86, CS_MODE_32 if pe.FILE_HEADER.Machine == 0x14c else CS_MODE_64)
    md.detail = False
    base = pe.OPTIONAL_HEADER.ImageBase
    blob = read_bytes(pe, rva, max_bytes)
    va = base + rva
    out = []
    for ins in md.disasm(blob, va):
        out.append(f"  0x{ins.address:08x}  {ins.bytes.hex():<20} {ins.mnemonic} {ins.op_str}")
        if stop_at_ret and ins.mnemonic.lower() in STOP_MNEMONICS:
            break
    return out


def list_exports(pe: pefile.PE):
    if not hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
        print("(no exports)")
        return
    for sym in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        name = sym.name.decode("latin-1") if sym.name else "<noname>"
        print(f"  ord {sym.ordinal:>4}  RVA 0x{sym.address:08x}  {name}")


def main(argv):
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    pe_path = argv[0]
    pe = pefile.PE(pe_path, fast_load=False)

    target = argv[1]
    if target == "--list":
        list_exports(pe)
        return 0

    max_bytes = 0x400
    stop_at_ret = True
    if "--bytes" in argv:
        i = argv.index("--bytes")
        max_bytes = int(argv[i + 1], 0)
        stop_at_ret = False

    if target.startswith("0x"):
        rva = int(target, 16)
        label = f"RVA {target}"
    else:
        rva = find_export(pe, target)
        if rva is None:
            print(f"export not found: {target}", file=sys.stderr)
            return 1
        label = target

    print(f"=== {Path(pe_path).name} : {label} (RVA 0x{rva:08x}, "
          f"VA 0x{pe.OPTIONAL_HEADER.ImageBase + rva:08x}) ===")
    sec = section_for_rva(pe, rva)
    if sec:
        nm = sec.Name.rstrip(b'\x00').decode('latin-1')
        print(f"section: {nm}\n")
    for line in disasm(pe, rva, max_bytes, stop_at_ret):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
