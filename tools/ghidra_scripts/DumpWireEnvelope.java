// Round-4 Ghidra script for j2534_interface.dll.
// Goal: surface the on-wire envelope by chasing two routes:
//   (a) FUN_1001d270  — the bidirectional "send-and-wait" helper used by both
//       write_transport and read_transport.
//   (b) the I/O drain thread that actually calls device_write_async (FUN_1003dca0).
// Lists callers of FUN_1003dca0 and GetQueuedCompletionStatus so we can identify
// the IOCP pump function, then decompiles the suspects.
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
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.symbol.SymbolIterator;
import ghidra.program.model.symbol.SymbolTable;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class DumpWireEnvelope extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Program program = currentProgram;
        long base = program.getImageBase().getOffset();
        String outPath = System.getenv("GHIDRA_DUMP_OUT");
        if (outPath == null) outPath = program.getExecutablePath() + ".envelope.md";
        File outFile = new File(outPath);
        outFile.getParentFile().mkdirs();
        PrintWriter out = new PrintWriter(new FileWriter(outFile));

        out.println("# Ghidra wire envelope — " + program.getName());
        out.println();
        out.println("Round 4: chase the bytes-on-wire format via send-and-wait helper + IOCP drain thread.");
        out.println();

        FunctionManager fm = program.getFunctionManager();
        SymbolTable st = program.getSymbolTable();
        ReferenceManager rm = program.getReferenceManager();
        Listing listing = program.getListing();

        // 1. Callers of device_write_async (FUN_1003dca0)
        out.println("## Callers of device_write_async (FUN_1003dca0 / WriteFile)");
        out.println();
        Address dwa = program.getAddressFactory().getDefaultAddressSpace().getAddress(base + 0x3dca0);
        Function dwaFn = fm.getFunctionAt(dwa);
        Set<Long> drainCandidates = new LinkedHashSet<>();
        if (dwaFn == null) {
            out.println("_(device_write_async not found)_");
        } else {
            ReferenceIterator it = rm.getReferencesTo(dwa);
            while (it.hasNext()) {
                Reference r = it.next();
                Function caller = fm.getFunctionContaining(r.getFromAddress());
                String cn = caller == null ? "<no func>" : caller.getName();
                long entry = caller == null ? 0 : caller.getEntryPoint().getOffset();
                out.println("- 0x" + r.getFromAddress() + "  ←  " + cn + " @ 0x" + Long.toHexString(entry));
                if (caller != null) drainCandidates.add(entry);
            }
        }
        out.println();

        // 2. Callers of GetQueuedCompletionStatus (the IOCP wait)
        out.println("## Callers of GetQueuedCompletionStatus (IOCP pump)");
        out.println();
        SymbolIterator gqcs = st.getSymbols("GetQueuedCompletionStatus");
        while (gqcs.hasNext()) {
            Symbol s = gqcs.next();
            Reference[] refs = s.getReferences();
            for (Reference r : refs) {
                Function caller = fm.getFunctionContaining(r.getFromAddress());
                if (caller == null) continue;
                String cn = caller.getName();
                long entry = caller.getEntryPoint().getOffset();
                out.println("- 0x" + r.getFromAddress() + "  ←  " + cn + " @ 0x" + Long.toHexString(entry));
                drainCandidates.add(entry);
            }
        }
        out.println();

        // 3. Callers of CreateThread (where I/O threads spawn)
        out.println("## Callers of CreateThread");
        out.println();
        SymbolIterator cts = st.getSymbols("CreateThread");
        while (cts.hasNext()) {
            Symbol s = cts.next();
            Reference[] refs = s.getReferences();
            for (Reference r : refs) {
                Function caller = fm.getFunctionContaining(r.getFromAddress());
                if (caller == null) continue;
                String cn = caller.getName();
                long entry = caller.getEntryPoint().getOffset();
                out.println("- 0x" + r.getFromAddress() + "  ←  " + cn + " @ 0x" + Long.toHexString(entry));
            }
        }
        out.println();

        // 4. Decompile targets:  FUN_1001d270 (send-and-wait) + each drain candidate
        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(program);

        Map<String, Long> fixedTargets = new LinkedHashMap<>();
        fixedTargets.put("send_and_wait (FUN_1001d270 — used by both transports)", base + 0x1d270);

        for (Map.Entry<String, Long> e : fixedTargets.entrySet()) {
            decompileFunction(out, decomp, fm, listing, rm, e.getKey(), e.getValue());
        }

        out.println("## IOCP drain / device_write_async caller(s) — auto-detected");
        out.println();
        int decompCount = 0;
        for (Long t : drainCandidates) {
            if (decompCount >= 6) break;
            decompileFunction(out, decomp, fm, listing, rm,
                    "FUN_" + Long.toHexString(t), t);
            decompCount++;
        }

        out.close();
        println("[dump] wrote " + outFile.getAbsolutePath());
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

        // Strings
        out.println("**Strings referenced (max 30):**");
        int strs = 0;
        AddressIterator it = f.getBody().getAddresses(true);
        while (it.hasNext() && strs < 30) {
            Address ax = it.next();
            Reference[] refs = rm.getReferencesFrom(ax);
            for (Reference r : refs) {
                Address to = r.getToAddress();
                Data d = listing.getDataAt(to);
                if (d != null && d.hasStringValue()) {
                    StringDataInstance sdi = StringDataInstance.getStringDataInstance(d);
                    String v = sdi == null ? d.getDefaultValueRepresentation() : sdi.getStringValue();
                    if (v != null && v.length() > 0) {
                        out.println("- 0x" + ax + " → 0x" + to + "  `" +
                                v.replace("\n","\\n").replace("\r","\\r") + "`");
                        if (++strs >= 30) break;
                    }
                }
            }
        }
        if (strs == 0) out.println("- _(none)_");
        out.println();

        DecompileResults dr = decomp.decompileFunction(f, 90, monitor);
        out.println("```c");
        if (dr != null && dr.getDecompiledFunction() != null) {
            out.println(dr.getDecompiledFunction().getC());
        } else {
            out.println("// decompile failed");
        }
        out.println("```");
        out.println();
    }
}
