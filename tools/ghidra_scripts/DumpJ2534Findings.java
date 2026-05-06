// Ghidra post-analysis script for j2534_interface.dll.
// Decompiles the real-impl addresses behind each J2534 export, lists
// xrefs to USB/serial-relevant Win32 imports, and writes a markdown
// report to the path in the GHIDRA_DUMP_OUT env var (or beside the program).
//
// @category Chipsoft_RE
// @runtime Java

import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.listing.Program;
import ghidra.program.model.symbol.ExternalReference;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceManager;
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.symbol.SymbolIterator;
import ghidra.program.model.symbol.SymbolTable;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class DumpJ2534Findings extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Program program = currentProgram;
        long base = program.getImageBase().getOffset();
        println("[dump] image base = " + Long.toHexString(base));

        String outPath = System.getenv("GHIDRA_DUMP_OUT");
        if (outPath == null) {
            outPath = program.getExecutablePath() + ".findings.md";
        }
        File outFile = new File(outPath);
        outFile.getParentFile().mkdirs();
        PrintWriter out = new PrintWriter(new FileWriter(outFile));

        out.println("# Ghidra findings — " + program.getName());
        out.println();
        out.println("- Image base: 0x" + Long.toHexString(base));
        out.println("- Language: " + program.getLanguage().getLanguageID());
        out.println();

        // 1. List exports
        out.println("## Exports");
        out.println();
        SymbolTable st = program.getSymbolTable();
        SymbolIterator exports = st.getAllSymbols(true);
        List<String> expRows = new ArrayList<>();
        while (exports.hasNext()) {
            Symbol s = exports.next();
            if (s.isExternalEntryPoint()) {
                expRows.add(String.format("- `%s` @ 0x%s", s.getName(), s.getAddress().toString()));
            }
        }
        Collections.sort(expRows);
        for (String r : expRows) out.println(r);
        out.println();

        // 2. Decompile target functions (J2534 real impls + the context helper)
        Map<String, Long> targets = new LinkedHashMap<>();
        if (program.getName().toLowerCase().contains("j2534_interface")) {
            targets.put("ctx_helper",          base + 0x6f40);
            targets.put("PassThruOpen_impl",   base + 0x4a00);
            targets.put("PassThruConnect_impl",base + 0x4f20);
            targets.put("PassThruDisconnect_impl", base + 0x51d0);
            targets.put("PassThruReadMsgs_impl",   base + 0x5390);
            targets.put("PassThruWriteMsgs_impl",  base + 0x5680);
            targets.put("PassThruStartPeriodicMsg_impl", base + 0x5970);
            targets.put("PassThruIoctl_impl",  base + 0x70a0);
        }

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(program);

        FunctionManager fm = program.getFunctionManager();
        out.println("## Decompiled targets");
        out.println();
        for (Map.Entry<String, Long> e : targets.entrySet()) {
            Address addr = program.getAddressFactory().getDefaultAddressSpace().getAddress(e.getValue());
            Function f = fm.getFunctionAt(addr);
            if (f == null) {
                f = fm.getFunctionContaining(addr);
            }
            out.println("### " + e.getKey() + " — 0x" + Long.toHexString(e.getValue()));
            out.println();
            if (f == null) {
                out.println("_(no function found at this address)_");
                out.println();
                continue;
            }
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

        // 3. xrefs to interesting Win32 imports
        String[] interesting = {
            "CreateFileA", "CreateFileW", "WriteFile", "ReadFile", "DeviceIoControl",
            "GetCommState", "SetCommState", "SetCommTimeouts", "PurgeComm",
            "GetOverlappedResult"
        };
        out.println("## Callers of key Win32 imports");
        out.println();
        ReferenceManager rm = program.getReferenceManager();
        for (String name : interesting) {
            SymbolIterator it = st.getSymbols(name);
            while (it.hasNext()) {
                Symbol s = it.next();
                if (!(s.getObject() instanceof ghidra.program.model.listing.Function) &&
                    !s.isExternal() && s.getSymbolType() != ghidra.program.model.symbol.SymbolType.LABEL &&
                    s.getSymbolType() != ghidra.program.model.symbol.SymbolType.FUNCTION) {
                    continue;
                }
                Reference[] refs = s.getReferences();
                if (refs.length == 0) continue;
                out.println("### " + name + " — " + refs.length + " refs");
                int shown = 0;
                for (Reference r : refs) {
                    Address from = r.getFromAddress();
                    Function caller = fm.getFunctionContaining(from);
                    String cname = caller == null ? "<no func>" : caller.getName() + " @ 0x" + caller.getEntryPoint();
                    out.println("- 0x" + from + "  ←  " + cname);
                    if (++shown >= 20) {
                        out.println("- ... (" + (refs.length - shown) + " more)");
                        break;
                    }
                }
                out.println();
            }
        }

        out.close();
        println("[dump] wrote " + outFile.getAbsolutePath());
    }
}
