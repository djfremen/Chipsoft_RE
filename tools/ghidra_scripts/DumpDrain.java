// Round-4b: chase caller(s) of FUN_1003bb10 (the only caller of device_write_async).
// That caller is the drain — it serializes a STRUCT_MESSAGE into wire bytes
// and feeds them to FUN_1003bb10. If the wire is just raw STRUCT_MESSAGE, we'll
// see a single-buffer descriptor with len 0x1038 here.
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
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.symbol.ReferenceManager;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.LinkedHashSet;
import java.util.Set;

public class DumpDrain extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Program program = currentProgram;
        long base = program.getImageBase().getOffset();
        String outPath = System.getenv("GHIDRA_DUMP_OUT");
        if (outPath == null) outPath = program.getExecutablePath() + ".drain.md";
        PrintWriter out = new PrintWriter(new FileWriter(new File(outPath)));

        out.println("# Ghidra drain — caller of FUN_1003bb10 (the bytes-to-WriteFile bridge)");
        out.println();

        FunctionManager fm = program.getFunctionManager();
        ReferenceManager rm = program.getReferenceManager();
        Listing listing = program.getListing();

        // Walk back two levels: callers of 1003bb10, then their callers (max 6 funcs).
        Address start = program.getAddressFactory().getDefaultAddressSpace().getAddress(base + 0x3bb10);
        Set<Long> level1 = new LinkedHashSet<>();
        ReferenceIterator it = rm.getReferencesTo(start);
        out.println("## Direct callers of FUN_1003bb10");
        out.println();
        while (it.hasNext()) {
            Reference r = it.next();
            Function caller = fm.getFunctionContaining(r.getFromAddress());
            if (caller == null) continue;
            long entry = caller.getEntryPoint().getOffset();
            level1.add(entry);
            out.println("- 0x" + r.getFromAddress() + "  ←  " + caller.getName() + " @ 0x" + Long.toHexString(entry));
        }
        out.println();

        Set<Long> level2 = new LinkedHashSet<>();
        out.println("## Callers of those callers (one level up)");
        out.println();
        for (Long fnVa : level1) {
            Address addr = program.getAddressFactory().getDefaultAddressSpace().getAddress(fnVa);
            Function f = fm.getFunctionAt(addr);
            if (f == null) continue;
            out.println("### Callers of FUN_" + Long.toHexString(fnVa));
            ReferenceIterator rit = rm.getReferencesTo(addr);
            while (rit.hasNext()) {
                Reference r = rit.next();
                Function caller = fm.getFunctionContaining(r.getFromAddress());
                if (caller == null) continue;
                long entry = caller.getEntryPoint().getOffset();
                level2.add(entry);
                out.println("- 0x" + r.getFromAddress() + "  ←  " + caller.getName() + " @ 0x" + Long.toHexString(entry));
            }
            out.println();
        }

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(program);

        out.println("## Decompiles — direct callers");
        out.println();
        for (Long t : level1) decompileFunction(out, decomp, fm, listing, rm, "FUN_" + Long.toHexString(t), t);

        out.println("## Decompiles — second-level (max 4)");
        out.println();
        int n = 0;
        for (Long t : level2) {
            if (n >= 4) break;
            decompileFunction(out, decomp, fm, listing, rm, "FUN_" + Long.toHexString(t), t);
            n++;
        }

        out.close();
        println("[dump] wrote " + outPath);
    }

    private void decompileFunction(PrintWriter out, DecompInterface decomp,
            FunctionManager fm, Listing listing, ReferenceManager rm,
            String label, long va) {
        Address addr = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(va);
        Function f = fm.getFunctionAt(addr);
        if (f == null) f = fm.getFunctionContaining(addr);
        out.println("### " + label + " — 0x" + Long.toHexString(va));
        out.println();
        if (f == null) { out.println("_(no function found)_"); out.println(); return; }

        out.println("**Strings referenced (max 25):**");
        int strs = 0;
        AddressIterator ait = f.getBody().getAddresses(true);
        while (ait.hasNext() && strs < 25) {
            Address ax = ait.next();
            Reference[] refs = rm.getReferencesFrom(ax);
            for (Reference r : refs) {
                Data d = listing.getDataAt(r.getToAddress());
                if (d != null && d.hasStringValue()) {
                    StringDataInstance sdi = StringDataInstance.getStringDataInstance(d);
                    String v = sdi == null ? d.getDefaultValueRepresentation() : sdi.getStringValue();
                    if (v != null && v.length() > 0) {
                        out.println("- 0x" + ax + " → 0x" + r.getToAddress() + "  `" +
                                v.replace("\n","\\n").replace("\r","\\r") + "`");
                        if (++strs >= 25) break;
                    }
                }
            }
        }
        if (strs == 0) out.println("- _(none)_");
        out.println();

        DecompileResults dr = decomp.decompileFunction(f, 90, monitor);
        out.println("```c");
        if (dr != null && dr.getDecompiledFunction() != null) out.println(dr.getDecompiledFunction().getC());
        else out.println("// decompile failed");
        out.println("```");
        out.println();
    }
}
