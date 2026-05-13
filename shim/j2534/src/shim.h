// j2534_interface shim — common header.
//
// Mirrors the cstech2win shim layout. All translation units include this.

#ifndef J2534_SHIM_H
#define J2534_SHIM_H

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdint.h>

// SAE J2534 calling convention on 32-bit Windows is WINAPI (__stdcall).
#define J2534API WINAPI

// ---- Logging -----------------------------------------------------------------
// One log file per process; opened lazily on first call.
// Logs are pipe-delimited: ms_since_attach | wall_clock_ms | tid | event | detail
//
// The wall_clock_ms column lets us merge this log against a concurrently
// running cstech2win_shim log on the same host.
extern void shim_log_init(void);
extern void shim_log(const char* fmt, ...);
extern void shim_log_hex(const char* tag, const void* buf, size_t len);

// ---- Real-DLL handle ---------------------------------------------------------
extern HMODULE g_hRealDll;

#endif // J2534_SHIM_H
