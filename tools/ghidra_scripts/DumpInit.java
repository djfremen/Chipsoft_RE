// Round 6d: dump FUN_10010550 (the giant init function — likely contains the
// log-path prologue) and the three options.json initializer functions
// (containing references at 0x10001ac2, 0x10001772, 0x100013f2). These should
// give us: the base log path, the JSON parser flow, and per-tier defaults.
//
// @category Chipsoft_RE
// @runtime Java

import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressIterator;
import ghidra.program.model.data.StringDataInstance;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.listing.Program;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceManager;
import ghidra.program.model.address.AddressSet;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.LinkedHashSet;
import java.util.Set;

public class DumpInit extends GhidraScript {

    private static final long[] CANDIDATES = {
        0x10010550L,   // big init fn — may contain log builder prologue
        0x100013f0L,   // CRT init #1 — actually decompile what's around 0x100013f2
        0x10001770L,   // CRT init #2
        0x10001ac0L,   // CRT init #3
        0x10010280L,   // FUN_10010280 — uses opcode 0x20 per opcode-summary, lives near init
        0x100101b0L,   // a few more init candidates
        0x10010250L,
    };

    @Override
    protected void run() throws Exception {
        Program program = currentProgram;
        FunctionManager fm = program.getFunctionManager();
        Listing listing = program.getListing();

        String outPath = System.getenv("GHIDRA_DUMP_OUT");
        if (outPath == null) outPath = program.getExecutablePath() + ".init.md";
        PrintWriter out = new PrintWriter(new FileWriter(new File(outPath)));

        out.println("# Init / log-path / JSON parse decompiles");
        out.println();

        // Try to disassemble suspicious addresses if not already.
        for (long va : CANDIDATES) {
            Address a = addr(va);
            if (listing.getInstructionAt(a) == null) {
                try { disassemble(a); }
                catch (Exception ex) { /* continue */ }
            }
            // Try to create a function at the address if there isn't one.
            if (fm.getFunctionAt(a) == null) {
                try {
                    createFunction(a, "ConfigInit_" + Long.toHexString(va));
                } catch (Exception ex) { /* continue */ }
            }
        }

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(program);

        for (long va : CANDIDATES) {
            Address a = addr(va);
            Function f = fm.getFunctionContaining(a);
            if (f == null) {
                out.println("## (no function at 0x" + Long.toHexString(va) + ")");
                out.println();
                continue;
            }
            decompile(out, decomp, f);
        }

        out.close();
        println("[init] wrote " + outPath);
    }

    private void decompile(PrintWriter out, DecompInterface decomp, Function f) {
        long e = f.getEntryPoint().getOffset();
        out.println("## " + f.getName() + " @ 0x" + Long.toHexString(e));
        out.println();

        Listing listing = currentProgram.getListing();
        ReferenceManager rm = currentProgram.getReferenceManager();
        out.println("**Strings referenced (max 60):**");
        int strs = 0;
        AddressIterator ait = f.getBody().getAddresses(true);
        Set<String> seen = new LinkedHashSet<>();
        while (ait.hasNext() && strs < 60) {
            Address ax = ait.next();
            Reference[] refs = rm.getReferencesFrom(ax);
            for (Reference r : refs) {
                Data d = listing.getDataAt(r.getToAddress());
                if (d == null || !d.hasStringValue()) continue;
                StringDataInstance sdi = StringDataInstance.getStringDataInstance(d);
                if (sdi == null) continue;
                String v = sdi.getStringValue();
                if (v == null || v.isEmpty()) continue;
                if (seen.add(v + "@" + r.getToAddress())) {
                    out.println("- 0x" + ax + " → 0x" + r.getToAddress() + "  `" +
                                v.replace("\n", "\\n").replace("\r", "\\r") + "`");
                    if (++strs >= 60) break;
                }
            }
        }
        if (strs == 0) out.println("- _(none)_");
        out.println();

        DecompileResults dr = decomp.decompileFunction(f, 180, monitor);
        out.println("```c");
        if (dr != null && dr.getDecompiledFunction() != null) {
            out.println(dr.getDecompiledFunction().getC());
        } else {
            out.println("// decompile failed");
        }
        out.println("```");
        out.println();
    }

    private Address addr(long va) {
        return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(va);
    }
}
