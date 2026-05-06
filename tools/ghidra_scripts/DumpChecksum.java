// Decompile FUN_100340c0 (the wire-frame checksum) and the read-bytes helper
// FUN_10039cb0 to confirm the read side mirrors the write framing.
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
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;

public class DumpChecksum extends GhidraScript {
    @Override
    protected void run() throws Exception {
        Program program = currentProgram;
        long base = program.getImageBase().getOffset();
        String outPath = System.getenv("GHIDRA_DUMP_OUT");
        if (outPath == null) outPath = program.getExecutablePath() + ".checksum.md";
        PrintWriter out = new PrintWriter(new FileWriter(new File(outPath)));
        FunctionManager fm = program.getFunctionManager();
        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(program);

        long[] targets = { base + 0x340c0, base + 0x39cb0 /* read helper */, base + 0x10cb90 /* hashed earlier - placeholder */ };
        String[] names = { "checksum FUN_100340c0", "read_bytes FUN_10039cb0", "extra" };

        for (int i = 0; i < 2; i++) {
            Address addr = program.getAddressFactory().getDefaultAddressSpace().getAddress(targets[i]);
            Function f = fm.getFunctionAt(addr);
            if (f == null) f = fm.getFunctionContaining(addr);
            out.println("## " + names[i] + " @ 0x" + Long.toHexString(targets[i]));
            out.println();
            if (f == null) { out.println("_(not found)_"); out.println(); continue; }
            DecompileResults dr = decomp.decompileFunction(f, 60, monitor);
            out.println("```c");
            if (dr != null && dr.getDecompiledFunction() != null) out.println(dr.getDecompiledFunction().getC());
            out.println("```");
            out.println();
        }
        out.close();
        println("[dump] wrote " + outPath);
    }
}
