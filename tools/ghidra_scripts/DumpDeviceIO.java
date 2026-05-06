// Round-2 Ghidra post-analysis script for j2534_interface.dll.
// Decompiles the device-I/O layer (the functions one level under the
// J2534 export real-impls) and dumps any .rdata strings reachable from
// them. Writes a markdown report to GHIDRA_DUMP_OUT.
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
import java.util.LinkedHashMap;
import java.util.Map;

public class DumpDeviceIO extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Program program = currentProgram;
        long base = program.getImageBase().getOffset();
        String outPath = System.getenv("GHIDRA_DUMP_OUT");
        if (outPath == null) outPath = program.getExecutablePath() + ".deviceio.md";
        File outFile = new File(outPath);
        outFile.getParentFile().mkdirs();
        PrintWriter out = new PrintWriter(new FileWriter(outFile));

        out.println("# Ghidra device-I/O layer — " + program.getName());
        out.println();
        out.println("Round 2: the layer between PassThru*_impl and the Win32 serial APIs.");
        out.println();

        Map<String, Long> targets = new LinkedHashMap<>();
        targets.put("write_framer (called by PassThruWriteMsgs_impl)",  base + 0x321a0);
        targets.put("read_framer  (called by PassThruReadMsgs_impl)",   base + 0x1a540);
        targets.put("device_open  (CreateFileA + Comm setup)",          base + 0x39460);
        targets.put("device_reconfig (GetCommState + SetCommState)",    base + 0x39800);
        targets.put("device_write_async (WriteFile + GetOverlappedResult)", base + 0x3dca0);
        targets.put("device_read  (ReadFile, non-CRT)",                 base + 0x392f0);
        targets.put("purge_a (PurgeComm)",                              base + 0x18990);
        targets.put("purge_b (PurgeComm)",                              base + 0x18ba0);

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(program);

        FunctionManager fm = program.getFunctionManager();
        Listing listing = program.getListing();
        ReferenceManager rm = program.getReferenceManager();

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

            // String references reachable inside this function body
            out.println("**Strings referenced from this function:**");
            out.println();
            int stringsFound = 0;
            AddressIterator it = f.getBody().getAddresses(true);
            while (it.hasNext() && stringsFound < 30) {
                Address a = it.next();
                Reference[] refs = rm.getReferencesFrom(a);
                for (Reference r : refs) {
                    Address to = r.getToAddress();
                    Data d = listing.getDataAt(to);
                    if (d != null && d.hasStringValue()) {
                        StringDataInstance sdi = StringDataInstance.getStringDataInstance(d);
                        String v = sdi == null ? d.getDefaultValueRepresentation() : sdi.getStringValue();
                        if (v != null && v.length() > 0) {
                            out.println("- 0x" + a + " → 0x" + to + "  `" +
                                        v.replace("\n","\\n").replace("\r","\\r") + "`");
                            stringsFound++;
                        }
                    }
                }
            }
            if (stringsFound == 0) out.println("- _(none)_");
            out.println();

            // Decompiled C
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

        out.close();
        println("[dump] wrote " + outFile.getAbsolutePath());
    }
}
