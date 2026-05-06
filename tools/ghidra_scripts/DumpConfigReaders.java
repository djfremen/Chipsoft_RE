// Round 6b: dump the three options.json reader blocks at 0x10001353,
// 0x100016d3, 0x10001a23 (file offsets 0x753/0xad3/0xe23) plus the
// log-sink builder containing 0x10011aa4. These were located via raw
// imm32-load byte search in DumpConfig output; Ghidra's xref analyzer
// missed them because the references load via PUSH imm32 from inside
// templated C++ static initializers.
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

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.LinkedHashSet;
import java.util.Set;

public class DumpConfigReaders extends GhidraScript {

    private static final long[] TARGETS = {
        0x10001353L,  // block 1 — first reader
        0x100016d3L,  // block 2 — second reader
        0x10001a23L,  // block 3 — third reader
        0x10011aa4L,  // log-sink builder (already partially seen in DumpConfig)
    };

    @Override
    protected void run() throws Exception {
        Program program = currentProgram;
        FunctionManager fm = program.getFunctionManager();
        ReferenceManager rm = program.getReferenceManager();
        Listing listing = program.getListing();

        String outPath = System.getenv("GHIDRA_DUMP_OUT");
        if (outPath == null) outPath = program.getExecutablePath() + ".configreaders.md";
        PrintWriter out = new PrintWriter(new FileWriter(new File(outPath)));

        out.println("# Ghidra config readers — three options.json sites + log builder");
        out.println();

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(program);

        for (long va : TARGETS) {
            Address a = addr(va);
            Function f = fm.getFunctionContaining(a);
            if (f == null) {
                out.println("## (no function containing 0x" + Long.toHexString(va) + ")");
                out.println();
                continue;
            }
            long entry = f.getEntryPoint().getOffset();
            out.println("## " + f.getName() + " @ 0x" + Long.toHexString(entry) +
                        " (containing 0x" + Long.toHexString(va) + ")");
            out.println();

            // String literals referenced from this function — with addresses.
            out.println("**String literals referenced (max 50):**");
            int strs = 0;
            AddressIterator ait = f.getBody().getAddresses(true);
            Set<String> seen = new LinkedHashSet<>();
            while (ait.hasNext() && strs < 50) {
                Address ax = ait.next();
                Reference[] refs = rm.getReferencesFrom(ax);
                for (Reference r : refs) {
                    Data d = listing.getDataAt(r.getToAddress());
                    if (d == null || !d.hasStringValue()) continue;
                    StringDataInstance sdi = StringDataInstance.getStringDataInstance(d);
                    if (sdi == null) continue;
                    String v = sdi.getStringValue();
                    if (v == null || v.isEmpty()) continue;
                    String key = v + "@" + r.getToAddress();
                    if (seen.add(key)) {
                        out.println("- 0x" + ax + " → 0x" + r.getToAddress() + "  `" +
                                v.replace("\n", "\\n").replace("\r", "\\r") + "`");
                        if (++strs >= 50) break;
                    }
                }
            }
            if (strs == 0) out.println("- _(none)_");
            out.println();

            // Outgoing function calls (which boost helpers etc.)
            out.println("**Outgoing function calls:**");
            Set<String> callees = new LinkedHashSet<>();
            for (Function c : f.getCalledFunctions(monitor)) {
                callees.add(c.getName() + " @ 0x" + Long.toHexString(c.getEntryPoint().getOffset()));
            }
            if (callees.isEmpty()) {
                out.println("- _(none)_");
            } else {
                for (String c : callees) out.println("- " + c);
            }
            out.println();

            DecompileResults dr = decomp.decompileFunction(f, 120, monitor);
            out.println("```c");
            if (dr != null && dr.getDecompiledFunction() != null) {
                out.println(dr.getDecompiledFunction().getC());
            } else {
                out.println("// decompile failed");
            }
            out.println("```");
            out.println();
        }

        out.close();
        println("[configreaders] wrote " + outPath);
    }

    private Address addr(long va) {
        return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(va);
    }
}
