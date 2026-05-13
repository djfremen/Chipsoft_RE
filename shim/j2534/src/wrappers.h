// Hand-written instrumented wrappers for the J2534 PassThru* exports.
//
// We instrument the calls that carry semantic info we care about:
//   PassThruOpen         — adapter device handshake
//   PassThruConnect      — protocol selection + channel ID
//   PassThruIoctl        — config/init/clear ops
//   PassThruStartMsgFilter — filter pattern + mask
//   PassThruWriteMsgs    — outgoing UDS / CAN frames
//   PassThruReadMsgs     — incoming frames with hardware timestamp
//
// The remaining 7 exports (Close, Disconnect, ReadVersion, GetLastError,
// SetProgrammingVoltage, StartPeriodicMsg, StopPeriodicMsg, StopMsgFilter)
// are auto-generated as naked-jmp forwarders by gen_shim.py.

#ifndef J2534_SHIM_WRAPPERS_H
#define J2534_SHIM_WRAPPERS_H

#include "shim.h"
#include "j2534.h"

extern FARPROC g_real_PassThruOpen;
extern FARPROC g_real_PassThruConnect;
extern FARPROC g_real_PassThruIoctl;
extern FARPROC g_real_PassThruStartMsgFilter;
extern FARPROC g_real_PassThruWriteMsgs;
extern FARPROC g_real_PassThruReadMsgs;

void resolve_instrumented_exports(HMODULE hReal);

#endif
