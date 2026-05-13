// SAE J2534 (PassThru API) type definitions.
//
// Reference: SAE J2534-1 (2002) and J2534-2 (2006). Conventions taken from
// the Drewtech / OpenPort SDK headers, which are the de facto standard
// across J2534 vendors. Our shim only needs the structs + IDs to log
// argument values; we don't implement any J2534 logic ourselves.

#ifndef J2534_H
#define J2534_H

#include <stdint.h>

// Standard PassThru message struct — same layout across all J2534 vendors.
// Always 4152 bytes total (sizeof on 32-bit Windows).
typedef struct {
    unsigned long ProtocolID;
    unsigned long RxStatus;
    unsigned long TxFlags;
    unsigned long Timestamp;       // microseconds since adapter open
    unsigned long DataSize;
    unsigned long ExtraDataIndex;
    unsigned char Data[4128];
} PASSTHRU_MSG;

// SCONFIG used by PassThruIoctl(SET_CONFIG / GET_CONFIG)
typedef struct {
    unsigned long Parameter;
    unsigned long Value;
} SCONFIG;

typedef struct {
    unsigned long NumOfParams;
    SCONFIG*      ConfigPtr;
} SCONFIG_LIST;

typedef struct {
    unsigned long NumOfBytes;
    unsigned char *BytePtr;
} SBYTE_ARRAY;

// Protocol IDs (J2534-1 §6.2)
#define PROTO_J1850VPW       1
#define PROTO_J1850PWM       2
#define PROTO_ISO9141        3
#define PROTO_ISO14230       4
#define PROTO_CAN            5
#define PROTO_ISO15765       6
#define PROTO_SCI_A_ENGINE   7
#define PROTO_SCI_A_TRANS    8
#define PROTO_SCI_B_ENGINE   9
#define PROTO_SCI_B_TRANS   10

// Filter types (J2534-1 §6.3)
#define FILTER_PASS         1
#define FILTER_BLOCK        2
#define FILTER_FLOW_CONTROL 3

// IOCTL IDs (J2534-1 §6.6)
#define IOCTL_GET_CONFIG          0x01
#define IOCTL_SET_CONFIG          0x02
#define IOCTL_READ_VBATT          0x03
#define IOCTL_FIVE_BAUD_INIT      0x04
#define IOCTL_FAST_INIT           0x05
#define IOCTL_CLEAR_TX_BUFFER     0x07
#define IOCTL_CLEAR_RX_BUFFER     0x08
#define IOCTL_CLEAR_PERIODIC_MSGS 0x09
#define IOCTL_CLEAR_MSG_FILTERS   0x0A
#define IOCTL_CLEAR_FUNCT_MSG_LOOKUP_TABLE 0x0B
#define IOCTL_ADD_TO_FUNCT_MSG_LOOKUP_TABLE 0x0C
#define IOCTL_DELETE_FROM_FUNCT_MSG_LOOKUP_TABLE 0x0D
#define IOCTL_READ_PROG_VOLTAGE   0x0E

// SCONFIG parameter IDs (J2534-1 §6.5) — most commonly seen
#define CONFIG_DATA_RATE       0x01
#define CONFIG_LOOPBACK        0x03
#define CONFIG_NODE_ADDRESS    0x04
#define CONFIG_NETWORK_LINE    0x05
#define CONFIG_P1_MIN          0x06
#define CONFIG_P1_MAX          0x07
#define CONFIG_P2_MIN          0x08
#define CONFIG_P2_MAX          0x09
#define CONFIG_P3_MIN          0x0A
#define CONFIG_P3_MAX          0x0B
#define CONFIG_P4_MIN          0x0C
#define CONFIG_P4_MAX          0x0D
#define CONFIG_W0              0x0E
#define CONFIG_W1              0x0F
#define CONFIG_W2              0x10
#define CONFIG_W3              0x11
#define CONFIG_W4              0x12
#define CONFIG_W5              0x13
#define CONFIG_TIDLE           0x14
#define CONFIG_TINIL           0x15
#define CONFIG_TWUP            0x16
#define CONFIG_PARITY          0x17

// Error codes the real DLL may return — useful for logging
#define STATUS_NOERROR         0x00
#define ERR_NOT_SUPPORTED      0x01
#define ERR_INVALID_CHANNEL_ID 0x02
#define ERR_INVALID_PROTOCOL_ID 0x03
#define ERR_NULL_PARAMETER     0x04
#define ERR_DEVICE_NOT_CONNECTED 0x08
#define ERR_TIMEOUT            0x09
#define ERR_INVALID_MSG        0x0A
#define ERR_BUFFER_EMPTY       0x10
#define ERR_BUFFER_FULL        0x11
#define ERR_BUFFER_OVERFLOW    0x12

// RxStatus bits (J2534-1 §6.4)
#define RX_TX_INDICATION       0x01  // this is a TX echo, not a real RX
#define RX_START_OF_MESSAGE    0x02
#define RX_BREAK_RECEIVED      0x04
#define RX_RX_BREAK_RECEIVED   0x04  // alias
#define RX_TX_DONE             0x08
#define RX_ISO15765_PADDING_ERR 0x10
#define RX_ISO15765_ADDR_TYPE  0x80
#define RX_CAN_29BIT_ID        0x100

// TxFlags bits (J2534-1 §6.5)
#define TX_ISO15765_FRAME_PAD  0x40
#define TX_ISO15765_ADDR_TYPE  0x80
#define TX_CAN_29BIT_ID        0x100
#define TX_WAIT_P3_MIN_ONLY    0x200
#define TX_SCI_TX_VOLTAGE      0x800000

#endif // J2534_H
