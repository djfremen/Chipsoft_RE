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
        // PDU_IT_RESULT items carry response bytes via pData -> PDU_RESULT_DATA.
        // Gating on ItemType (not EventType) — Chipsoft uses EventType=0xF3 for
        // its result events, observed in the 2026-05-06 capture.
        if (ev->ItemType == 0x1300 /* PDU_IT_RESULT */ && ev->pData) {
            PDU_RESULT_DATA_MIN* rd = (PDU_RESULT_DATA_MIN*)ev->pData;
            if (rd->pDataBytes && rd->NumDataBytes > 0 && rd->NumDataBytes <= 4096) {
                shim_log_hex("RSP-PDU", rd->pDataBytes, rd->NumDataBytes);
            }
        }
    }
    return r;
}

T_PDU_ERROR PDUAPI PDURegisterEventCallback(UNUM32 hMod, UNUM32 hCLL,
                                            void (PDUAPI *cb)(UNUM32, UNUM32, void*)) {
    shim_log("CALL |PDURegisterEventCallback|hMod=0x%08X hCLL=0x%08X cb=%p",
             hMod, hCLL, (void*)cb);
    T_PDU_ERROR r = ((fn_PDURegisterEventCallback)g_real_PDURegisterEventCallback)(hMod, hCLL, cb);
    shim_log("RET  |PDURegisterEventCallback|err=%u", r);
    return r;
}
