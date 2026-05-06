// Round-3 Ghidra script for j2534_interface.dll.
// Walks down from the framers to find where bytes meet the wire.
// Decompiles FUN_1001a140 (write transport) and FUN_10016e10 (read transport),
// dumps the COM-port path format string at DAT_100e50a0, and follows the call
// chain from the write transport one more level toward FUN_1003dca0 (WriteFile).
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
import ghidra.program.model.mem.Memory;
import ghidra.program.model.mem.MemoryAccessException;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class DumpTransport extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Program program = currentProgram;
        long base = program.getImageBase().getOffset();
        String outPath = System.getenv("GHIDRA_DUMP_OUT");
        if (outPath == null) outPath = program.getExecutablePath() + ".transport.md";
        File outFile = new File(outPath);
        outFile.getParentFile().mkdirs();
        PrintWriter out = new PrintWriter(new FileWriter(outFile));

        out.println("# Ghidra transport-layer — " + program.getName());
        out.println();
        out.println("Round 3: between framers and Win32 serial APIs.");
        out.println();

        Map<String, Long> targets = new LinkedHashMap<>();
        targets.put("write_transport (called by write_framer FUN_100321a0)", base + 0x1a140);
        targets.put("read_transport  (called by read_framer  FUN_1001a540)", base + 0x16e10);

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(program);

        // Dump suspected path format string and a generous window around it
        out.println("## .rdata strings near suspected path-format references");
        out.println();
        long[] suspectedConstants = { base + 0xe50a0, base + 0xe5000, base + 0xe5020, base + 0xe5040, base + 0xe5060, base + 0xe5080 };
        Memory mem = program.getMemory();
        for (long va : suspectedConstants) {
            Address a = program.getAddressFactory().getDefaultAddressSpace().getAddress(va);
            try {
                byte[] b = new byte[64];
                mem.getBytes(a, b);
                StringBuilder sb = new StringBuilder();
                for (byte by : b) {
                    if (by == 0) break;
                    if (by >= 0x20 && by < 0x7f) sb.append((char) by);
                    else sb.append(String.format("\\x%02x", by & 0xff));
                }
                out.println("- 0x" + Long.toHexString(va) + "  `" + sb + "`");
            } catch (MemoryAccessException ex) {
                out.println("- 0x" + Long.toHexString(va) + "  (unreadable)");
            }
        }
        out.println();

        FunctionManager fm = program.getFunctionManager();
        Listing listing = program.getListing();
        ReferenceManager rm = program.getReferenceManager();

        // Decompile the two transport functions, then chase outgoing CALL targets
        // one level deep so we can see whether they reach FUN_1003dca0 / FUN_100392f0.
        List<Long> chasedCalls = new ArrayList<>();
        for (Map.Entry<String, Long> e : targets.entrySet()) {
            Address addr = program.getAddressFactory().getDefaultAddressSpace().getAddress(e.getValue());
            Function f = fm.getFunctionAt(addr);
            if (f == null) f = fm.getFunctionContaining(addr);
            out.println("## " + e.getKey() + " — 0x" + Long.toHexString(e.getValue()));
            out.println();
            if (f == null) {
                out.println("_(no function found)_");
                out.println();
                continue;
            }

            // Strings + outgoing CALL targets
            out.println("**Strings referenced:**");
            int strs = 0;
            AddressIterator it = f.getBody().getAddresses(true);
            List<Long> outgoing = new ArrayList<>();
            while (it.hasNext()) {
                Address ax = it.next();
                Reference[] refs = rm.getReferencesFrom(ax);
                for (Reference r : refs) {
                    Address to = r.getToAddress();
                    if (r.getReferenceType().isCall()) {
                        long calledVa = to.getOffset();
                        if (!outgoing.contains(calledVa)) outgoing.add(calledVa);
                    }
                    Data d = listing.getDataAt(to);
                    if (d != null && d.hasStringValue() && strs < 20) {
                        StringDataInstance sdi = StringDataInstance.getStringDataInstance(d);
                        String v = sdi == null ? d.getDefaultValueRepresentation() : sdi.getStringValue();
                        if (v != null && v.length() > 0) {
                            out.println("- 0x" + ax + " → 0x" + to + "  `" +
                                        v.replace("\n","\\n").replace("\r","\\r") + "`");
                            strs++;
                        }
                    }
                }
            }
            if (strs == 0) out.println("- _(none)_");
            out.println();
            out.println("**Outgoing calls (unique):**");
            int oc = 0;
            for (Long t : outgoing) {
                Function callee = fm.getFunctionAt(program.getAddressFactory().getDefaultAddressSpace().getAddress(t));
                String cn = callee == null ? "<no function>" : callee.getName();
                out.println("- 0x" + Long.toHexString(t) + "  " + cn);
                if (oc < 4 && cn.startsWith("FUN_")) chasedCalls.add(t);
                oc++;
            }
            out.println();

            DecompileResults dr = decomp.decompileFunction(f, 60, monitor);
            out.println("```c");
            if (dr != null && dr.getDecompiledFunction() != null) {
                out.println(dr.getDecompiledFunction().getC());
            } else {
                out.println("// decompile failed");
            }
            out.println("```");
            out.println();
        }

        // Chase one level deeper: decompile the first few internal calls
        // each transport function makes (limited to 6 to keep output manageable).
        out.println("## One level deeper — first few callees of the transport funcs");
        out.println();
        int chased = 0;
        for (Long t : chasedCalls) {
            if (chased >= 6) break;
            Function f = fm.getFunctionAt(program.getAddressFactory().getDefaultAddressSpace().getAddress(t));
            if (f == null) continue;
            out.println("### FUN_" + Long.toHexString(t) + " (size " + f.getBody().getNumAddresses() + " bytes)");
            DecompileResults dr = decomp.decompileFunction(f, 60, monitor);
            out.println("```c");
            if (dr != null && dr.getDecompiledFunction() != null) {
                out.println(dr.getDecompiledFunction().getC());
            } else {
                out.println("// decompile failed");
            }
            out.println("```");
            out.println();
            chased++;
        }

        out.close();
        println("[dump] wrote " + outFile.getAbsolutePath());
    }
}
