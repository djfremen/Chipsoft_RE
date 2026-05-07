// CSTech2Win shim — instrumented exports.
//
// These six functions get hand-written __stdcall wrappers that log args and
// output buffers around a passthrough call to the real DLL.
//
// Function signatures are from ISO 22900-2 (D-PDU API). We only declare the
// minimum struct layout needed to extract the bytes we care about — full
// struct definitions live in ISO22900-2 if/when we need them.
//
// The most valuable byte capture is in PDUStartComPrimitive: pCoPData carries
// the raw request bytes Tech2Win wants sent to the ECU (e.g. $27 $01 for
// SecurityAccess requestSeed). That's where the SAS/IMMO custom $Level will
// surface, if it exists.
//
// Phase 1 (this file): log args + request buffer. Sufficient to identify which
// $Level Tech2Win invokes and prove the shim wiring works.
//
// Phase 2 (TODO): deep-decode PDUGetEventItem's PDU_RESULT_DATA->pDataBytes
// to capture seed/key response bytes.

#include "shim.h"
#include "wrappers.h"

// ---- typedefs for the 6 instrumented exports --------------------------------
typedef T_PDU_ERROR (PDUAPI *fn_PDUConstruct)(CHAR8* OptionStr, void* pAPITag);
typedef T_PDU_ERROR (PDUAPI *fn_PDUDestruct)(void);
typedef T_PDU_ERROR (PDUAPI *fn_PDUIoCtl)(UNUM32 hMod, UNUM32 hCLL, UNUM32 IoCtlCommandId,
                                          void* pInputData, void** pOutputData);
typedef T_PDU_ERROR (PDUAPI *fn_PDUStartComPrimitive)(UNUM32 hMod, UNUM32 hCLL,
                                                     UNUM32 CoPType, UNUM32 CoPDataSize,
                                                     UNUM8* pCoPData, void* pCopCtrlData,
                                                     void* pCoPTag, UNUM32* phCoP);
typedef T_PDU_ERROR (PDUAPI *fn_PDUGetEventItem)(UNUM32 hMod, UNUM32 hCLL, void** pEventItem);
typedef T_PDU_ERROR (PDUAPI *fn_PDURegisterEventCallback)(UNUM32 hMod, UNUM32 hCLL,
                                                         void (PDUAPI *cb)(UNUM32, UNUM32, void*));

FARPROC g_real_PDUConstruct = NULL;
FARPROC g_real_PDUDestruct = NULL;
FARPROC g_real_PDUIoCtl = NULL;
FARPROC g_real_PDUStartComPrimitive = NULL;
FARPROC g_real_PDUGetEventItem = NULL;
FARPROC g_real_PDURegisterEventCallback = NULL;

void resolve_instrumented_exports(HMODULE hReal) {
    g_real_PDUConstruct           = GetProcAddress(hReal, "PDUConstruct");
    g_real_PDUDestruct            = GetProcAddress(hReal, "PDUDestruct");
    g_real_PDUIoCtl               = GetProcAddress(hReal, "PDUIoCtl");
    g_real_PDUStartComPrimitive   = GetProcAddress(hReal, "PDUStartComPrimitive");
    g_real_PDUGetEventItem        = GetProcAddress(hReal, "PDUGetEventItem");
    g_real_PDURegisterEventCallback = GetProcAddress(hReal, "PDURegisterEventCallback");
}

// ---- Wrappers ---------------------------------------------------------------

T_PDU_ERROR PDUAPI PDUConstruct(CHAR8* OptionStr, void* pAPITag) {
    shim_log("CALL |PDUConstruct|opt='%s' tag=%p", OptionStr ? OptionStr : "(null)", pAPITag);
    T_PDU_ERROR r = ((fn_PDUConstruct)g_real_PDUConstruct)(OptionStr, pAPITag);
    shim_log("RET  |PDUConstruct|err=%u", r);
    return r;
}

T_PDU_ERROR PDUAPI PDUDestruct(void) {
    shim_log("CALL |PDUDestruct|");
    T_PDU_ERROR r = ((fn_PDUDestruct)g_real_PDUDestruct)();
    shim_log("RET  |PDUDestruct|err=%u", r);
    return r;
}

T_PDU_ERROR PDUAPI PDUIoCtl(UNUM32 hMod, UNUM32 hCLL, UNUM32 IoCtlCommandId,
                            void* pInputData, void** pOutputData) {
    shim_log("CALL |PDUIoCtl|hMod=0x%08X hCLL=0x%08X cmd=0x%08X",
             hMod, hCLL, IoCtlCommandId);
    T_PDU_ERROR r = ((fn_PDUIoCtl)g_real_PDUIoCtl)(hMod, hCLL, IoCtlCommandId,
                                                    pInputData, pOutputData);
    shim_log("RET  |PDUIoCtl|err=%u", r);
    return r;
}

T_PDU_ERROR PDUAPI PDUStartComPrimitive(UNUM32 hMod, UNUM32 hCLL,
                                        UNUM32 CoPType, UNUM32 CoPDataSize,
                                        UNUM8* pCoPData, void* pCopCtrlData,
                                        void* pCoPTag, UNUM32* phCoP) {
    // CoPType 0x8001=PDU_COPT_STARTCOMM, 0x8002=PDU_COPT_STOPCOMM,
    //         0x8010=PDU_COPT_SENDRECV (this is what carries diag requests),
    //         0x8011=PDU_COPT_DELAY, 0x8020=PDU_COPT_UPDATEPARAM
    shim_log("CALL |PDUStartComPrimitive|hMod=0x%08X hCLL=0x%08X CoPType=0x%04X size=%u",
             hMod, hCLL, CoPType, CoPDataSize);
    if (pCoPData && CoPDataSize > 0 && CoPDataSize <= 4096) {
        shim_log_hex("REQ-PDU", pCoPData, CoPDataSize);
    }
    T_PDU_ERROR r = ((fn_PDUStartComPrimitive)g_real_PDUStartComPrimitive)(
        hMod, hCLL, CoPType, CoPDataSize, pCoPData, pCopCtrlData, pCoPTag, phCoP);
    shim_log("RET  |PDUStartComPrimitive|err=%u hCoP=0x%08X",
             r, (phCoP && r == 0) ? *phCoP : 0);
    return r;
}

// PDU_EVENT_ITEM minimal layout (ISO 22900-2). We only read what we need.
typedef struct {
    UNUM32  ItemType;
    UNUM32  EventType;     // 0x0001=DATA_AVAILABLE, 0x0010=PDU_EVT_RESULT
    UNUM32  hCop;
    UNUM32  Timestamp;
    void*   pCopTag;
    void*   pData;         // for RESULT events: PDU_RESULT_DATA*
} PDU_EVENT_ITEM_MIN;

typedef struct {
    UNUM32  RxFlag;
    UNUM32  TimingFlag;
    UNUM32  ExtraInfo;
    UNUM32  UniqueRespIdentifier;
    UNUM32  AcceptanceId;
    UNUM32  Timestamp;
    UNUM32  NumDataBytes;
    UNUM8*  pDataBytes;
    UNUM32  NumExtraInfo;
    void*   pExtraInfo;
} PDU_RESULT_DATA_MIN;

T_PDU_ERROR PDUAPI PDUGetEventItem(UNUM32 hMod, UNUM32 hCLL, void** pEventItem) {
    T_PDU_ERROR r = ((fn_PDUGetEventItem)g_real_PDUGetEventItem)(hMod, hCLL, pEventItem);
    if (r == 0 && pEventItem && *pEventItem) {
        PDU_EVENT_ITEM_MIN* ev = (PDU_EVENT_ITEM_MIN*)*pEventItem;
        shim_log("EVT  |PDUGetEventItem|hMod=0x%08X hCLL=0x%08X "
                 "ItemType=0x%X EventType=0x%X hCop=0x%08X ts=%u",
                 hMod, hCLL, ev->ItemType, ev->EventType, ev->hCop, ev->Timestamp);
        // For result events, dereference and dump the byte payload —
        // this is where the seed/key response lives.
        // Chipsoft uses EventType as a monotonic counter, not ISO 22900-2's
        // 0x0010 constant, so we gate on ItemType alone. Some 0x1300 events
        // may have pData pointing to non-PDU_RESULT_DATA memory, so we wrap
        // in SEH to survive bad pointers without crashing Tech2Win.
        if (ev->ItemType == 0x1300 /* PDU_IT_RESULT */) {
            UNUM8* item_bytes = (UNUM8*)*pEventItem;
            __try {
                // Dump exactly 24 bytes (standard ISO size) to see what's inside.
                shim_log_hex("EVT-RAW", item_bytes, 24);
            } __except(EXCEPTION_EXECUTE_HANDLER) {
                shim_log("ERR  |PDUGetEventItem|fault dumping event item raw bytes");
            }
            // Phase 2 layout discovery (see HANDOFF.md):
            // The 2026-05-06 64-byte dump showed Chipsoft's PDU_EVENT_ITEM has
            // a variant layout. For EventType=0x114, response bytes are inline
            // at offset 32. For EventType=0xF3 (the $27 0B path we're tracking),
            // they're not inline — they live behind a pointer stored at offset
            // 12 or 16. Dump both with SEH guards. Whichever reliably contains
            // the UDS response bytes (look for "67 0B" after $27 0B requests)
            // is our seed source for the next decoder iteration.
            UNUM8* p12 = NULL;
            UNUM8* p16 = NULL;
            __try {
                p12 = *(UNUM8**)(item_bytes + 12);
                p16 = *(UNUM8**)(item_bytes + 16);
            } __except(EXCEPTION_EXECUTE_HANDLER) {
                p12 = NULL; p16 = NULL;
            }
            if (p12) {
                __try {
                    shim_log_hex("PTR12-DEREF", p12, 32);
                } __except(EXCEPTION_EXECUTE_HANDLER) {
                    shim_log("ERR  |PDUGetEventItem|ptr12 fault p12=%p", p12);
                }
            }
            if (p16) {
                __try {
                    shim_log_hex("PTR16-DEREF", p16, 32);
                } __except(EXCEPTION_EXECUTE_HANDLER) {
                    shim_log("ERR  |PDUGetEventItem|ptr16 fault p16=%p", p16);
                }
                // 2026-05-06 run 4 finding (HANDOFF.md Q1):
                // PTR16-DEREF reveals a {length, ptr_to_data} table at offset 0:
                //   bytes 0-3 = length (often 4, matching $27 0B response size)
                //   bytes 4-7 = pointer to actual UDS response payload
                // Dereference that inner pointer to extract the seed bytes.
                UNUM8* pPayload = NULL;
                __try {
                    pPayload = *(UNUM8**)(p16 + 4);
                } __except(EXCEPTION_EXECUTE_HANDLER) {
                    pPayload = NULL;
                }
                if (pPayload) {
                    __try {
                        shim_log_hex("RSP-PAYLOAD", pPayload, 32);
                    } __except(EXCEPTION_EXECUTE_HANDLER) {
                        shim_log("ERR  |PDUGetEventItem|payload fault pPayload=%p", pPayload);
                    }
                }
                // Some events have a second {length, ptr} pair at offset 16
                // of the table — dump that too in case the seed lives there.
                UNUM8* pPayload2 = NULL;
                __try {
                    pPayload2 = *(UNUM8**)(p16 + 20);
                } __except(EXCEPTION_EXECUTE_HANDLER) {
                    pPayload2 = NULL;
                }
                if (pPayload2) {
                    __try {
                        shim_log_hex("RSP-PAYLOAD2", pPayload2, 32);
                    } __except(EXCEPTION_EXECUTE_HANDLER) {
                        shim_log("ERR  |PDUGetEventItem|payload2 fault pPayload2=%p", pPayload2);
                    }
                }
            }
        }
    }
    return r;
}

// ---- Callback trampolines ---------------------------------------------------
//
// 2026-05-07 finding (HANDOFF.md option 3): SecurityAccess responses ($27 $0B
// seed/key) do NOT surface in PDUGetEventItem result events. They arrive via
// the callback Tech2 registers through PDURegisterEventCallback. The callback
// signature is __stdcall void (UNUM32 hMod, UNUM32 hCLL, void* pData).
//
// To intercept, we substitute the caller's cb with one of N pre-generated
// trampolines. Each trampoline knows its slot index at compile time and uses
// it to look up the real cb in g_cb_slots[]. The dispatcher logs args + the
// pData buffer (which carries the response bytes), then forwards to the real
// cb. Tech2 only registered 3 callbacks in the run-5 capture, so 16 slots is
// generous.

typedef void (PDUAPI *cb_t)(UNUM32 hMod, UNUM32 hCLL, void* pData);

#define MAX_CB_SLOTS 16

static struct {
    cb_t   real_cb;
    UNUM32 hMod;
    UNUM32 hCLL;
    int    used;
} g_cb_slots[MAX_CB_SLOTS];
static int g_cb_count = 0;
static CRITICAL_SECTION g_cb_lock;
static int g_cb_lock_initialized = 0;

static void common_cb_dispatch(int slot, UNUM32 hMod, UNUM32 hCLL, void* pData) {
    shim_log("CB   |fired|slot=%d hMod=0x%08X hCLL=0x%08X pData=%p",
             slot, hMod, hCLL, pData);
    // Dump the pData buffer — this is where the seed bytes live for $27 $0B.
    // Size unknown; 64 is generous enough to contain any UDS response plus
    // whatever metadata Chipsoft prepends/appends.
    if (pData) {
        __try {
            shim_log_hex("CB-DATA", pData, 64);
        } __except (EXCEPTION_EXECUTE_HANDLER) {
            shim_log("ERR  |CB|data fault pData=%p", pData);
        }
    }
    cb_t real = g_cb_slots[slot].real_cb;
    if (real) {
        real(hMod, hCLL, pData);
    }
}

#define DEFINE_CB_TRAMP(N) \
    static void PDUAPI cb_tramp_##N(UNUM32 hMod, UNUM32 hCLL, void* pData) { \
        common_cb_dispatch(N, hMod, hCLL, pData); \
    }

DEFINE_CB_TRAMP(0)  DEFINE_CB_TRAMP(1)  DEFINE_CB_TRAMP(2)  DEFINE_CB_TRAMP(3)
DEFINE_CB_TRAMP(4)  DEFINE_CB_TRAMP(5)  DEFINE_CB_TRAMP(6)  DEFINE_CB_TRAMP(7)
DEFINE_CB_TRAMP(8)  DEFINE_CB_TRAMP(9)  DEFINE_CB_TRAMP(10) DEFINE_CB_TRAMP(11)
DEFINE_CB_TRAMP(12) DEFINE_CB_TRAMP(13) DEFINE_CB_TRAMP(14) DEFINE_CB_TRAMP(15)

static cb_t g_tramps[MAX_CB_SLOTS] = {
    cb_tramp_0,  cb_tramp_1,  cb_tramp_2,  cb_tramp_3,
    cb_tramp_4,  cb_tramp_5,  cb_tramp_6,  cb_tramp_7,
    cb_tramp_8,  cb_tramp_9,  cb_tramp_10, cb_tramp_11,
    cb_tramp_12, cb_tramp_13, cb_tramp_14, cb_tramp_15,
};

T_PDU_ERROR PDUAPI PDURegisterEventCallback(UNUM32 hMod, UNUM32 hCLL,
                                            void (PDUAPI *cb)(UNUM32, UNUM32, void*)) {
    shim_log("CALL |PDURegisterEventCallback|hMod=0x%08X hCLL=0x%08X cb=%p",
             hMod, hCLL, (void*)cb);

    // Lazy-init the lock on first call (DllMain isn't always a safe place
    // to do this; this gets us the same effect with fewer constraints).
    if (!g_cb_lock_initialized) {
        InitializeCriticalSection(&g_cb_lock);
        g_cb_lock_initialized = 1;
    }

    cb_t passed_cb = (cb_t)cb;
    int slot = -1;
    EnterCriticalSection(&g_cb_lock);
    if (g_cb_count < MAX_CB_SLOTS && cb != NULL) {
        slot = g_cb_count++;
        g_cb_slots[slot].real_cb = passed_cb;
        g_cb_slots[slot].hMod = hMod;
        g_cb_slots[slot].hCLL = hCLL;
        g_cb_slots[slot].used = 1;
    }
    LeaveCriticalSection(&g_cb_lock);

    if (slot >= 0) {
        passed_cb = g_tramps[slot];
        shim_log("CB   |register|slot=%d real=%p tramp=%p", slot, (void*)cb, (void*)passed_cb);
    } else if (cb != NULL) {
        shim_log("WARN |register|no free slot, passing real cb through (cb=%p)", (void*)cb);
    }

    T_PDU_ERROR r = ((fn_PDURegisterEventCallback)g_real_PDURegisterEventCallback)(
        hMod, hCLL, (void (PDUAPI*)(UNUM32, UNUM32, void*))passed_cb);
    shim_log("RET  |PDURegisterEventCallback|err=%u", r);
    return r;
}
