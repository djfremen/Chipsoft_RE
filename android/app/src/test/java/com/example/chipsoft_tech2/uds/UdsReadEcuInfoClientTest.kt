package com.example.chipsoft_tech2.uds

import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class UdsReadEcuInfoClientTest {

    private fun open(t: FakeEcuTransport): FakeEcuTransport = t.also { it.open(500_000) }

    @Test
    fun singleFrame_asciiPid_returnsTrimmedString() {
        // Trionic 8 ECU hardware ID is 4 ASCII chars on the wire.
        // Wire shape: 06 5A 71 'A' 'B' 'C' 'D' 00
        val ecu = open(FakeEcuTransport(ecuIdData = mapOf(0x71 to "ABCD".toByteArray())))
        val client = UdsReadEcuInfoClient(ecu)

        val result = client.read(UdsReadEcuInfoClient.Pid.EcuHardware)

        assertTrue("expected Ascii, got $result", result is UdsReadEcuInfoClient.Result.Ascii)
        val ascii = result as UdsReadEcuInfoClient.Result.Ascii
        assertEquals(0x71, ascii.pid)
        assertEquals("ABCD", ascii.text)
        // Verify the request that went out: 02 1A 71 00 00 00 00 00
        assertEquals(1, ecu.sent.size)
        assertArrayEquals(
            byteArrayOf(0x02, 0x1A, 0x71, 0, 0, 0, 0, 0),
            ecu.sent[0].data,
        )
    }

    @Test
    fun singleFrame_binaryPid_returnsRawBytes() {
        // PI 0xB9 = "Subnet config list highspeed" — 2 raw bytes per Trionic8.cs::GetPIB9.
        val expected = byteArrayOf(0x12, 0x34)
        val ecu = open(FakeEcuTransport(ecuIdData = mapOf(0xB9 to expected)))
        val client = UdsReadEcuInfoClient(ecu)

        val result = client.read(UdsReadEcuInfoClient.Pid.SubnetHsConfig)

        assertTrue("expected Bytes, got $result", result is UdsReadEcuInfoClient.Result.Bytes)
        val bytes = result as UdsReadEcuInfoClient.Result.Bytes
        assertEquals(0xB9, bytes.pid)
        assertArrayEquals(expected, bytes.bytes)
    }

    @Test
    fun multiFrame_vin_isReassembled() {
        // VIN is 17 ASCII chars. UDS payload = 5A 90 V1..V17 = 19 bytes total.
        // ISO-TP: FF carries 4 payload bytes, then 2 CFs carry 7 + 6 = 13 bytes.
        val vin = "YS3FD49Y541012017"
        val ecu = open(FakeEcuTransport(ecuIdData = mapOf(0x90 to vin.toByteArray())))
        val client = UdsReadEcuInfoClient(ecu)

        val result = client.read(UdsReadEcuInfoClient.Pid.Vin)

        assertTrue("expected Ascii, got $result", result is UdsReadEcuInfoClient.Result.Ascii)
        val ascii = result as UdsReadEcuInfoClient.Result.Ascii
        assertEquals(vin, ascii.text)
        // Client should have sent the request + a flow-control frame.
        assertEquals(2, ecu.sent.size)
        assertEquals(0x02.toByte(), ecu.sent[0].data[0])     // request SF
        assertEquals(0x1A.toByte(), ecu.sent[0].data[1])
        assertEquals(0x90.toByte(), ecu.sent[0].data[2])
        assertEquals(0x30.toByte(), ecu.sent[1].data[0])     // CTS flow control
    }

    @Test
    fun unknownPid_returnsNegativeResponse() {
        // Empty ecuIdData → fake replies 7F 1A 31 (requestOutOfRange) for any PID.
        val ecu = open(FakeEcuTransport())
        val client = UdsReadEcuInfoClient(ecu)

        val result = client.readPid(0xFF)

        assertTrue("expected NegativeResponse, got $result", result is UdsReadEcuInfoClient.Result.NegativeResponse)
        val nr = result as UdsReadEcuInfoClient.Result.NegativeResponse
        assertEquals(0xFF, nr.pid)
        assertEquals(0x31, nr.nrc)
        assertEquals("requestOutOfRange", nr.message)
    }

    @Test
    fun silentEcu_returnsTransportError() {
        val ecu = open(FakeEcuTransport(behavior = FakeEcuTransport.Behavior.Silent))
        val client = UdsReadEcuInfoClient(ecu, timeoutMs = 50)

        val result = client.read(UdsReadEcuInfoClient.Pid.Vin)

        assertTrue("expected TransportError, got $result", result is UdsReadEcuInfoClient.Result.TransportError)
    }

    @Test
    fun trailingNullsAreStripped() {
        // Some SAAB PIDs return fixed-width fields with trailing NULs.
        val padded = byteArrayOf('A'.code.toByte(), 'B'.code.toByte(), 0, 0, 0)
        val ecu = open(FakeEcuTransport(ecuIdData = mapOf(0x71 to padded)))
        val client = UdsReadEcuInfoClient(ecu)

        val result = client.read(UdsReadEcuInfoClient.Pid.EcuHardware) as UdsReadEcuInfoClient.Result.Ascii

        assertEquals("AB", result.text)
        // Raw bytes are still preserved unmodified for callers that want them.
        assertArrayEquals(padded, result.raw)
    }
}
