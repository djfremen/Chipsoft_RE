#!/usr/bin/env python3
"""High-level summary of a PE32 binary: arch, sections, imports, exports.

Usage: pe_summary.py <path-to-pe>
"""
import sys
from pathlib import Path
import pefile


def main(path: str) -> int:
    pe = pefile.PE(path, fast_load=False)
    print(f"=== {Path(path).name} ===")
    print(f"Machine:        0x{pe.FILE_HEADER.Machine:04x} "
          f"({'x86' if pe.FILE_HEADER.Machine == 0x14c else 'x64' if pe.FILE_HEADER.Machine == 0x8664 else '?'})")
    print(f"Image base:     0x{pe.OPTIONAL_HEADER.ImageBase:08x}")
    print(f"Entry point:    0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:08x} "
          f"(VA 0x{pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.AddressOfEntryPoint:08x})")
    print(f"Subsystem:      {pe.OPTIONAL_HEADER.Subsystem}")
    print(f"DLL char.:      0x{pe.OPTIONAL_HEADER.DllCharacteristics:04x}")

    print("\n-- Sections --")
    for s in pe.sections:
        name = s.Name.rstrip(b'\x00').decode('latin-1')
        print(f"  {name:<10} VA=0x{s.VirtualAddress:08x} "
              f"VSize=0x{s.Misc_VirtualSize:08x} "
              f"RawSize=0x{s.SizeOfRawData:08x} "
              f"flags=0x{s.Characteristics:08x}")

    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        print(f"\n-- Exports ({len(pe.DIRECTORY_ENTRY_EXPORT.symbols)}) --")
        for sym in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            name = sym.name.decode('latin-1') if sym.name else '<noname>'
            print(f"  ord {sym.ordinal:>4}  RVA 0x{sym.address:08x}  {name}")
    else:
        print("\n-- Exports --  (none)")

    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        print(f"\n-- Imports ({len(pe.DIRECTORY_ENTRY_IMPORT)} DLLs) --")
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            dll = entry.dll.decode('latin-1')
            print(f"  {dll}  ({len(entry.imports)} symbols)")
            for imp in entry.imports:
                nm = imp.name.decode('latin-1') if imp.name else f'ord_{imp.ordinal}'
                print(f"      {nm}")

    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
