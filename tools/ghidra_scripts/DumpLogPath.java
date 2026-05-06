// Round 6c: find the real entry point of the log-sink builder (Ghidra split
// it at 0x10011a99, but the prologue is earlier). Walk back from 0x10011a99
// looking for a function start, then decompile it. Also find readers of the
// global "options.json" string so we get the JSON open + parse site.
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
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.listing.Program;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.symbol.ReferenceManager;
import ghidra.program.model.scalar.Scalar;
import ghidra.program.model.address.AddressSet;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.TreeMap;

public class DumpLogPath extends GhidraScript {

    @Override
    protected void run() throws Exception {
        Program program = currentProgram;
        FunctionManager fm = program.getFunctionManager();
        ReferenceManager rm = program.getReferenceManager();
        Listing listing = program.getListing();

        String outPath = System.getenv("GHIDRA_DUMP_OUT");
        if (outPath == null) outPath = program.getExecutablePath() + ".logpath.md";
        PrintWriter out = new PrintWriter(new FileWriter(new File(outPath)));

        out.println("# Ghidra log-path resolution + JSON open site");
        out.println();

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(program);

        // ---------------------------------------------------------------------
        // 1. Find the function whose body actually contains the log-sink
        //    builder (\logs\ string ref at VA 0x10011aa4). Walk backward
        //    from 0x10011a99 looking for the nearest function START.
        // ---------------------------------------------------------------------
        long target = 0x10011aa4L;
        Function logBuilder = fm.getFunctionContaining(addr(target));
        if (logBuilder != null) {
            out.println("Function containing 0x" + Long.toHexString(target) +
                        ": " + logBuilder.getName() + " @ 0x" +
                        Long.toHexString(logBuilder.getEntryPoint().getOffset()));
            out.println();
        }

        // List nearby functions (5 before / 5 after) so we can see structure.
        out.println("## Functions near 0x10011aa4");
        out.println();
        FunctionIterator allFn = fm.getFunctions(true);
        List<Function> nearby = new ArrayList<>();
        while (allFn.hasNext()) {
            Function f = allFn.next();
            long e = f.getEntryPoint().getOffset();
            if (e >= 0x10010000L && e <= 0x10013000L) nearby.add(f);
        }
        for (Function f : nearby) {
            long e = f.getEntryPoint().getOffset();
            out.println("- " + f.getName() + " @ 0x" + Long.toHexString(e));
        }
        out.println();

        // ---------------------------------------------------------------------
        // 2. Decompile the function (or ones bracketing 0x10011aa4) so we see
        //    where the base path comes from.
        // ---------------------------------------------------------------------
        if (logBuilder != null) {
            decompile(out, decomp, logBuilder);
        }

        // ---------------------------------------------------------------------
        // 3. Find the JSON open / parse site: anything that references the
        //    global "options.json" string-storage object. The static
        //    initializers stored "options.json" at one of three .data slots
        //    (one per tier); find those addresses by walking the .data
        //    section for pointers TO 0x100e0714 and report any function
        //    that references those slots.
        // ---------------------------------------------------------------------
        out.println("## Search: refs to 'options.json' literal address (0x100e0714)");
        out.println();
        Address optAddr = addr(0x100e0714L);
        ReferenceIterator rit = rm.getReferencesTo(optAddr);
        Set<Long> refsFromFns = new LinkedHashSet<>();
        while (rit.hasNext()) {
            Reference r = rit.next();
            Function f = fm.getFunctionContaining(r.getFromAddress());
            String fname = f == null ? "(no function)" : f.getName() + " @ 0x" +
                           Long.toHexString(f.getEntryPoint().getOffset());
            out.println("- 0x" + r.getFromAddress() + " ← " + fname);
            if (f != null) refsFromFns.add(f.getEntryPoint().getOffset());
        }
        out.println();

        // ---------------------------------------------------------------------
        // 4. Search .data for pointers to 0x100e0714 (the global std::string
        //    objects that hold "options.json" and friends after CRT init).
        // ---------------------------------------------------------------------
        out.println("## .data slots holding 'options.json' pointer (raw scan)");
        out.println();
        // .data: VA 0x100fc000+0xee48
        byte[] needle = new byte[]{0x14, 0x07, 0x0e, 0x10};
        Address dataStart = addr(0x100fc000L);
        long dataLen = 0xee48L;
        List<Long> slotVAs = new ArrayList<>();
        for (long off = 0; off < dataLen - 4; off++) {
            byte[] buf = new byte[4];
            try {
                program.getMemory().getBytes(dataStart.add(off), buf);
            } catch (Exception ex) { continue; }
            if (buf[0] == needle[0] && buf[1] == needle[1] &&
                buf[2] == needle[2] && buf[3] == needle[3]) {
                long va = 0x100fc000L + off;
                slotVAs.add(va);
                out.println("- 0x" + Long.toHexString(va));
            }
        }
        out.println();

        // For each slot that holds "options.json", scan refs to its slot VA
        // (offset by -0x10 so we get the std::string object header, not the
        // pointer field — Boost-style strings have the data ptr at offset
        // 0x10 typically). Try -0, -4, -8, -0xc, -0x10.
        out.println("## Functions referencing the std::string slots holding 'options.json'");
        out.println();
        Set<Long> jsonRefFns = new LinkedHashSet<>();
        for (long va : slotVAs) {
            for (int delta : new int[]{0, -4, -8, -0xc, -0x10, -0x14, -0x18}) {
                long checkVA = va + delta;
                Address a = addr(checkVA);
                ReferenceIterator rit2 = rm.getReferencesTo(a);
                while (rit2.hasNext()) {
                    Reference r = rit2.next();
                    Function f = fm.getFunctionContaining(r.getFromAddress());
                    if (f == null) continue;
                    long e = f.getEntryPoint().getOffset();
                    if (jsonRefFns.add(e)) {
                        out.println("- 0x" + Long.toHexString(checkVA) +
                                    " (delta " + delta + ") ← " +
                                    f.getName() + " @ 0x" + Long.toHexString(e) +
                                    " (from 0x" + r.getFromAddress() + ")");
                    }
                }
            }
        }
        out.println();

        // Decompile each unique function found above.
        out.println("## Decompiles of options.json-referencing functions");
        out.println();
        for (long e : jsonRefFns) {
            Function f = fm.getFunctionAt(addr(e));
            if (f == null) continue;
            decompile(out, decomp, f);
        }

        out.close();
        println("[logpath] wrote " + outPath);
    }

    private void decompile(PrintWriter out, DecompInterface decomp, Function f) {
        long e = f.getEntryPoint().getOffset();
        out.println("### " + f.getName() + " @ 0x" + Long.toHexString(e));
        out.println();

        // Strings referenced from this function.
        Listing listing = currentProgram.getListing();
        ReferenceManager rm = currentProgram.getReferenceManager();
        out.println("**Strings referenced (max 40):**");
        int strs = 0;
        AddressIterator ait = f.getBody().getAddresses(true);
        Set<String> seen = new LinkedHashSet<>();
        while (ait.hasNext() && strs < 40) {
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
                    if (++strs >= 40) break;
                }
            }
        }
        if (strs == 0) out.println("- _(none)_");
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

    private Address addr(long va) {
        return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(va);
    }
}
