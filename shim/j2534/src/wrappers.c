// Hand-written instrumented wrappers for J2534 PassThru* exports.

#include "wrappers.h"

// Real-DLL function pointers
FARPROC g_real_PassThruOpen          = NULL;
FARPROC g_real_PassThruConnect       = NULL;
FARPROC g_real_PassThruIoctl         = NULL;
FARPROC g_real_PassThruStartMsgFilter = NULL;
FARPROC g_real_PassThruWriteMsgs     = NULL;
FARPROC g_real_PassThruReadMsgs      = NULL;

void resolve_instrumented_exports(HMODULE hReal) {
    g_real_PassThruOpen           = GetProcAddress(hReal, "PassThruOpen");
    g_real_PassThruConnect        = GetProcAddress(hReal, "PassThruConnect");
    g_real_PassThruIoctl          = GetProcAddress(hReal, "PassThruIoctl");
    g_real_PassThruStartMsgFilter = GetProcAddress(hReal, "PassThruStartMsgFilter");
    g_real_PassThruWriteMsgs      = GetProcAddress(hReal, "PassThruWriteMsgs");
    g_real_PassThruReadMsgs       = GetProcAddress(hReal, "PassThruReadMsgs");
}

// ---- Helpers ----------------------------------------------------------------
static const char* proto_name(unsigned long p) {
    switch (p) {
        case PROTO_J1850VPW:   return "J1850VPW";
        case PROTO_J1850PWM:   return "J1850PWM";
        case PROTO_ISO9141:    return "ISO9141";
        case PROTO_ISO14230:   return "ISO14230";
        case PROTO_CAN:        return "CAN";
        case PROTO_ISO15765:   return "ISO15765";
        case PROTO_SCI_A_ENGINE: return "SCI_A_ENGINE";
        case PROTO_SCI_A_TRANS:  return "SCI_A_TRANS";
        case PROTO_SCI_B_ENGINE: return "SCI_B_ENGINE";
        case PROTO_SCI_B_TRANS:  return "SCI_B_TRANS";
        default: return "?";
    }
}

static const char* ioctl_name(unsigned long id) {
    switch (id) {
        case IOCTL_GET_CONFIG: return "GET_CONFIG";
        case IOCTL_SET_CONFIG: return "SET_CONFIG";
        case IOCTL_READ_VBATT: return "READ_VBATT";
        case IOCTL_FIVE_BAUD_INIT: return "FIVE_BAUD_INIT";
        case IOCTL_FAST_INIT: return "FAST_INIT";
        case IOCTL_CLEAR_TX_BUFFER: return "CLEAR_TX_BUFFER";
        case IOCTL_CLEAR_RX_BUFFER: return "CLEAR_RX_BUFFER";
        case IOCTL_CLEAR_PERIODIC_MSGS: return "CLEAR_PERIODIC_MSGS";
        case IOCTL_CLEAR_MSG_FILTERS: return "CLEAR_MSG_FILTERS";
        case IOCTL_CLEAR_FUNCT_MSG_LOOKUP_TABLE: return "CLEAR_FUNCT_MSG_LOOKUP";
        case IOCTL_ADD_TO_FUNCT_MSG_LOOKUP_TABLE: return "ADD_FUNCT_MSG";
        case IOCTL_DELETE_FROM_FUNCT_MSG_LOOKUP_TABLE: return "DEL_FUNCT_MSG";
        case IOCTL_READ_PROG_VOLTAGE: return "READ_PROG_VOLTAGE";
        default: return "?";
    }
}

static const char* filter_name(unsigned long f) {
    switch (f) {
        case FILTER_PASS: return "PASS";
        case FILTER_BLOCK: return "BLOCK";
        case FILTER_FLOW_CONTROL: return "FLOW_CONTROL";
        default: return "?";
    }
}

static void log_msg(const char* tag, const PASSTHRU_MSG* m) {
    if (!m) {
        shim_log("%s|<null>", tag);
        return;
    }
    shim_log("%s|proto=%s(%lu) RxStatus=0x%08lX TxFlags=0x%08lX HwTs=%luus DataSize=%lu ExtraIdx=%lu",
             tag, proto_name(m->ProtocolID), m->ProtocolID,
             m->RxStatus, m->TxFlags, m->Timestamp, m->DataSize, m->ExtraDataIndex);
    unsigned long n = m->DataSize;
    if (n > sizeof(m->Data)) n = sizeof(m->Data);
    if (n > 0) shim_log_hex(tag, m->Data, n);
}

// ---- PassThruOpen ------------------------------------------------------------
__declspec(dllexport) long J2534API PassThruOpen(void* pName, unsigned long* pDeviceID) {
    shim_log("CALL |PassThruOpen|pName=%p", pName);
    typedef long (J2534API *fn_t)(void*, unsigned long*);
    long r = ((fn_t)g_real_PassThruOpen)(pName, pDeviceID);
    shim_log("RET  |PassThruOpen|rv=0x%lX DeviceID=%lu",
             r, pDeviceID ? *pDeviceID : 0);
    return r;
}

// ---- PassThruConnect ---------------------------------------------------------
__declspec(dllexport) long J2534API PassThruConnect(
    unsigned long DeviceID, unsigned long ProtocolID,
    unsigned long Flags, unsigned long BaudRate,
    unsigned long* pChannelID)
{
    shim_log("CALL |PassThruConnect|DeviceID=%lu Proto=%s(%lu) Flags=0x%lX Baud=%lu",
             DeviceID, proto_name(ProtocolID), ProtocolID, Flags, BaudRate);
    typedef long (J2534API *fn_t)(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long*);
    long r = ((fn_t)g_real_PassThruConnect)(DeviceID, ProtocolID, Flags, BaudRate, pChannelID);
    shim_log("RET  |PassThruConnect|rv=0x%lX ChannelID=%lu",
             r, pChannelID ? *pChannelID : 0);
    return r;
}

// ---- PassThruIoctl -----------------------------------------------------------
__declspec(dllexport) long J2534API PassThruIoctl(
    unsigned long ChannelID, unsigned long IoctlID,
    void* pInput, void* pOutput)
{
    shim_log("CALL |PassThruIoctl|ChannelID=%lu Ioctl=%s(0x%lX) pIn=%p pOut=%p",
             ChannelID, ioctl_name(IoctlID), IoctlID, pInput, pOutput);
    // For SET_CONFIG / GET_CONFIG, pInput is SCONFIG_LIST*
    if ((IoctlID == IOCTL_SET_CONFIG || IoctlID == IOCTL_GET_CONFIG) && pInput) {
        SCONFIG_LIST* sl = (SCONFIG_LIST*)pInput;
        shim_log("  | %s NumOfParams=%lu",
                 IoctlID == IOCTL_SET_CONFIG ? "SET_CONFIG" : "GET_CONFIG",
                 sl->NumOfParams);
        for (unsigned long i = 0; i < sl->NumOfParams && i < 32; i++) {
            shim_log("  |   [%lu] Param=0x%02lX Value=0x%lX",
                     i, sl->ConfigPtr[i].Parameter, sl->ConfigPtr[i].Value);
        }
    }
    typedef long (J2534API *fn_t)(unsigned long, unsigned long, void*, void*);
    long r = ((fn_t)g_real_PassThruIoctl)(ChannelID, IoctlID, pInput, pOutput);
    shim_log("RET  |PassThruIoctl|rv=0x%lX", r);
    if (r == 0 && IoctlID == IOCTL_GET_CONFIG && pInput) {
        SCONFIG_LIST* sl = (SCONFIG_LIST*)pInput;
        for (unsigned long i = 0; i < sl->NumOfParams && i < 32; i++) {
            shim_log("  | GET_CONFIG result [%lu] Param=0x%02lX Value=0x%lX",
                     i, sl->ConfigPtr[i].Parameter, sl->ConfigPtr[i].Value);
        }
    }
    return r;
}

// ---- PassThruStartMsgFilter --------------------------------------------------
__declspec(dllexport) long J2534API PassThruStartMsgFilter(
    unsigned long ChannelID, unsigned long FilterType,
    PASSTHRU_MSG* pMaskMsg, PASSTHRU_MSG* pPatternMsg,
    PASSTHRU_MSG* pFlowControlMsg, unsigned long* pFilterID)
{
    shim_log("CALL |PassThruStartMsgFilter|ChannelID=%lu FilterType=%s(%lu)",
             ChannelID, filter_name(FilterType), FilterType);
    log_msg("  Mask   ", pMaskMsg);
    log_msg("  Pattern", pPatternMsg);
    log_msg("  FlowCtl", pFlowControlMsg);
    typedef long (J2534API *fn_t)(unsigned long, unsigned long, PASSTHRU_MSG*, PASSTHRU_MSG*, PASSTHRU_MSG*, unsigned long*);
    long r = ((fn_t)g_real_PassThruStartMsgFilter)(ChannelID, FilterType,
                                                    pMaskMsg, pPatternMsg,
                                                    pFlowControlMsg, pFilterID);
    shim_log("RET  |PassThruStartMsgFilter|rv=0x%lX FilterID=%lu",
             r, pFilterID ? *pFilterID : 0);
    return r;
}

// ---- PassThruWriteMsgs -------------------------------------------------------
__declspec(dllexport) long J2534API PassThruWriteMsgs(
    unsigned long ChannelID, PASSTHRU_MSG* pMsg,
    unsigned long* pNumMsgs, unsigned long Timeout)
{
    unsigned long req = pNumMsgs ? *pNumMsgs : 0;
    shim_log("CALL |PassThruWriteMsgs|ChannelID=%lu NumMsgs=%lu Timeout=%lu",
             ChannelID, req, Timeout);
    for (unsigned long i = 0; i < req && i < 8; i++) {
        char tag[32];
        snprintf(tag, sizeof(tag), "TX[%lu]", i);
        log_msg(tag, &pMsg[i]);
    }
    typedef long (J2534API *fn_t)(unsigned long, PASSTHRU_MSG*, unsigned long*, unsigned long);
    long r = ((fn_t)g_real_PassThruWriteMsgs)(ChannelID, pMsg, pNumMsgs, Timeout);
    shim_log("RET  |PassThruWriteMsgs|rv=0x%lX Sent=%lu",
             r, pNumMsgs ? *pNumMsgs : 0);
    return r;
}

// ---- PassThruReadMsgs --------------------------------------------------------
__declspec(dllexport) long J2534API PassThruReadMsgs(
    unsigned long ChannelID, PASSTHRU_MSG* pMsg,
    unsigned long* pNumMsgs, unsigned long Timeout)
{
    unsigned long req = pNumMsgs ? *pNumMsgs : 0;
    // Don't log the request side — clients poll constantly and the log
    // would explode. Only log on the way out.
    typedef long (J2534API *fn_t)(unsigned long, PASSTHRU_MSG*, unsigned long*, unsigned long);
    long r = ((fn_t)g_real_PassThruReadMsgs)(ChannelID, pMsg, pNumMsgs, Timeout);
    unsigned long got = pNumMsgs ? *pNumMsgs : 0;
    if (got > 0 || r != 0) {
        shim_log("CALL/RET|PassThruReadMsgs|ChannelID=%lu ReqMsgs=%lu Timeout=%lu rv=0x%lX Got=%lu",
                 ChannelID, req, Timeout, r, got);
        for (unsigned long i = 0; i < got && i < 8; i++) {
            char tag[32];
            snprintf(tag, sizeof(tag), "RX[%lu]", i);
            log_msg(tag, &pMsg[i]);
        }
    }
    return r;
}
