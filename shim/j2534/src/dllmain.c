// j2534_interface shim — DLL entry point and lifecycle.
//
// On DLL_PROCESS_ATTACH:
//   1. Open the log file in %TEMP%\j2534_shim_<timestamp>.log
//   2. LoadLibrary("j2534_interface_real.dll") from the same dir as our DLL.
//      The real DLL must be renamed before install (move the original
//      j2534_interface.dll to j2534_interface_real.dll, then drop our shim
//      in its place named j2534_interface.dll).
//   3. Resolve all 13 PassThru* exports.
//
// On DLL_PROCESS_DETACH: close handles cleanly.

#include "shim.h"
#include "wrappers.h"
#include <string.h>

HMODULE g_hRealDll = NULL;

extern void resolve_passthrough_exports(HMODULE hReal);

static void load_real_dll(HINSTANCE hSelf) {
    char self_path[MAX_PATH] = {0};
    GetModuleFileNameA((HMODULE)hSelf, self_path, MAX_PATH);
    char* last_slash = strrchr(self_path, '\\');
    if (last_slash) *(last_slash + 1) = '\0';

    char real_path[MAX_PATH];
    snprintf(real_path, MAX_PATH, "%sj2534_interface_real.dll", self_path);

    g_hRealDll = LoadLibraryA(real_path);
    if (!g_hRealDll) {
        DWORD err = GetLastError();
        shim_log("FATAL|LoadLibrary failed for '%s' (err=%lu)", real_path, err);
        return;
    }
    shim_log("INIT |loaded real DLL from '%s'", real_path);

    resolve_passthrough_exports(g_hRealDll);
    resolve_instrumented_exports(g_hRealDll);
}

BOOL WINAPI DllMain(HINSTANCE hInstance, DWORD reason, LPVOID reserved) {
    (void)reserved;
    switch (reason) {
        case DLL_PROCESS_ATTACH:
            DisableThreadLibraryCalls(hInstance);
            shim_log_init();
            shim_log("INIT |DLL_PROCESS_ATTACH pid=%lu", GetCurrentProcessId());
            load_real_dll(hInstance);
            break;
        case DLL_PROCESS_DETACH:
            shim_log("EXIT |DLL_PROCESS_DETACH pid=%lu", GetCurrentProcessId());
            if (g_hRealDll) {
                FreeLibrary(g_hRealDll);
                g_hRealDll = NULL;
            }
            break;
    }
    return TRUE;
}
