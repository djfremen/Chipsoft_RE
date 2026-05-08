#!/usr/bin/env python3
"""
Scan j2534_interface.dll for every call site that invokes the send_and_wait
dispatcher (FUN_1001d270 by Ghidra naming) and extract the opcode constant
each caller passes. Output: { caller_func_addr: opcode_value }.

Approach:
  1. Locate every `call 0x1001d270` instruction in the .text section.
  2. For each, walk backward up to ~64 bytes looking for the opcode literal
     load — it's typically `push <imm>` or `mov edx/ecx/etc, <imm>` very close
     to the call (Chipsoft's wrappers are tiny one-shot dispatchers).
  3. If the calling instructions match the expected pattern, record (caller, opcode).
  4. Dump everything as a markdown table for cross-reference against the
     existing 24-opcode catalog.

This catches opcodes the original Ghidra round missed — anything reachable
from PassThruConnect / StartMsgFilter / etc. via paths we didn't explicitly trace.
"""

import struct
import sys
from collections import defaultdict
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

DLL_PATH = sys.argv[1] if len(sys.argv) > 1 else \
    '/Users/admin/.openclaw/workspace/Chipsoft_RE/CHIPSOFT_J2534_Pro_Driver/j2534_interface.dll'
SEND_AND_WAIT_VA = 0x1001d270   # from existing catalog notes

with open(DLL_PATH, 'rb') as f:
    data = f.read()

# Parse PE to find .text
pe_off = struct.unpack('<I', data[0x3c:0x40])[0]
n_sections = struct.unpack('<H', data[pe_off+0x6:pe_off+0x8])[0]
opt_size = struct.unpack('<H', data[pe_off+0x14:pe_off+0x16])[0]
sec_off = pe_off + 0x18 + opt_size
text = None
for i in range(n_sections):
    s = sec_off + i*0x28
    name = data[s:s+8].rstrip(b'\x00').decode('latin1')
    vaddr = struct.unpack('<I', data[s+0x0c:s+0x10])[0]
    vsize = struct.unpack('<I', data[s+0x08:s+0x0c])[0]
    rsize = struct.unpack('<I', data[s+0x10:s+0x14])[0]
    rptr  = struct.unpack('<I', data[s+0x14:s+0x18])[0]
    if name == '.text':
        text = (vaddr, vsize, rptr, rsize)
        text_va_base = 0x10000000 + vaddr
        break
assert text is not None
text_bytes = data[text[2]:text[2]+text[3]]
print(f"# .text VA={text_va_base:08X} size={text[1]:08X}", file=sys.stderr)

# Pass 1: find every `call <imm32>` whose target is SEND_AND_WAIT_VA.
# x86 near-call opcode is E8 followed by 4-byte signed displacement;
# target = next_insn_address + displacement.
md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True

call_sites = []  # list of VAs of `call send_and_wait`
for insn in md.disasm(text_bytes, text_va_base):
    if insn.mnemonic == 'call' and insn.op_str.startswith('0x'):
        try:
            tgt = int(insn.op_str, 16)
        except ValueError:
            continue
        if tgt == SEND_AND_WAIT_VA:
            call_sites.append(insn.address)

print(f"# {len(call_sites)} call sites to send_and_wait found", file=sys.stderr)

# Pass 2: for each call site, walk back up to N bytes and disassemble.
# Look for the opcode literal load. The send_and_wait signature (per
# notes/2026-05-05-ghidra-envelope.md) is something like:
#     FUN_1001d270(this, opcode, msg, len, out, timeout_ms)
# In x86 stdcall/thiscall, the args are pushed RIGHT-TO-LEFT before the call.
# So `opcode` (2nd arg) is one of the LATER pushes — the one immediately
# before `this` (which comes via ECX in thiscall).
# Heuristic: find the closest `push <small_imm>` (imm <= 0xFF) before the call.

LOOKBACK_BYTES = 96
results = []
for cs_va in call_sites:
    cs_off = cs_va - text_va_base
    start = max(0, cs_off - LOOKBACK_BYTES)
    chunk = text_bytes[start:cs_off]
    pushes_imm = []
    for ins in md.disasm(chunk, text_va_base + start):
        if ins.mnemonic == 'push' and ins.op_str.startswith('0x'):
            try:
                v = int(ins.op_str, 16)
                if v <= 0xFFFF:
                    pushes_imm.append((ins.address, v))
            except ValueError:
                pass
        elif ins.mnemonic == 'push' and ins.op_str.startswith('-0x'):
            pass
    # The opcode tends to be the SECOND push from the bottom (last is timeout
    # or out-buffer). Try last several and report.
    if pushes_imm:
        # Candidate: the last push that's <= 0xFF (one-byte opcode range)
        opcode_candidates = [(addr, v) for addr, v in pushes_imm if v <= 0xFF]
        results.append((cs_va, opcode_candidates))
    else:
        results.append((cs_va, []))

# Group by opcode value
by_opcode = defaultdict(list)
for cs_va, candidates in results:
    if not candidates:
        by_opcode['UNRESOLVED'].append((cs_va, []))
    else:
        # Use the LAST push of <= 0xFF as the strongest opcode candidate
        # (closest to the call → most likely the "stamp opcode" push)
        addr, v = candidates[-1]
        by_opcode[v].append((cs_va, candidates))

print()
print("# Opcode → call-site map (extracted from j2534_interface.dll)")
print()
print("| Opcode | # call sites | Notes |")
print("|---|---|---|")
for op in sorted(by_opcode.keys(), key=lambda x: (isinstance(x, str), x)):
    sites = by_opcode[op]
    if op == 'UNRESOLVED':
        label = 'UNRESOLVED'
    else:
        label = f'0x{op:02X}'
    sample = sites[0][0] if sites else 0
    print(f"| {label} | {len(sites)} | first call site VA = 0x{sample:08X} |")

print()
print("# Detail (call sites + nearby push history)")
for op in sorted(by_opcode.keys(), key=lambda x: (isinstance(x, str), x)):
    sites = by_opcode[op]
    label = 'UNRESOLVED' if op == 'UNRESOLVED' else f'0x{op:02X}'
    print(f"\n## opcode {label} — {len(sites)} call site(s)")
    for cs_va, candidates in sites[:5]:  # cap detail
        print(f"  call site VA: 0x{cs_va:08X}")
        for addr, v in candidates[-4:]:
            print(f"    push 0x{v:X} at 0x{addr:08X}")
    if len(sites) > 5:
        print(f"  ... and {len(sites)-5} more")
