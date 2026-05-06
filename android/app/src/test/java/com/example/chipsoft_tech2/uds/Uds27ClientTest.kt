package com.example.chipsoft_tech2.uds

import com.example.chipsoft_tech2.crypto.SaabSeedToKey
import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class Uds27ClientTest {

    private fun open(t: FakeEcuTransport): FakeEcuTransport = t.also { it.open(33333) }

    @Test
    fun happyPath_grantsAccess_andSendsCorrectKey() {
        // Use a captured seed → key pair so we can verify the wire bytes.
        val ecu = open(FakeEcuTransport(seed = 0x7F14, behavior = FakeEcuTransport.Behavior.HappyPath))
        val client = Uds27Client(ecu)

        val result = client.unlock(SaabSeedToKey.T8Level.L01)

        assertTrue("expected Granted, got $result", result is Uds27Client.Result.Granted)
        assertEquals("two frames sent (RequestSeed + SendKey)", 2, ecu.sent.size)

        // Frame 1: 02 27 01 00 00 00 00 00
        assertArrayEquals(
            byteArrayOf(0x02, 0x27, 0x01, 0, 0, 0, 0, 0),
            ecu.sent[0].data,
        )
        // Frame 2: 04 27 02 5D 80 00 00 00   (key for seed 0x7F14 = 0x5D80)
        assertArrayEquals(
            byteArrayOf(0x04, 0x27, 0x02, 0x5D, 0x80.toByte(), 0, 0, 0),
            ecu.sent[1].data,
        )
    }

    @Test
    fun alreadyGranted_whenEcmReturnsZeroSeed() {
        val ecu = open(FakeEcuTransport(behavior = FakeEcuTransport.Behavior.AlreadyGranted))
        val client = Uds27Client(ecu)

        val result = client.unlock()

        assertTrue("expected AlreadyGranted, got $result", result is Uds27Client.Result.AlreadyGranted)
        assertEquals("only RequestSeed sent — no SendKey needed", 1, ecu.sent.size)
    }

    @Test
    fun deniedWithInvalidKey_propagatesNrc35() {
        val ecu = open(FakeEcuTransport(behavior = FakeEcuTransport.Behavior.BadKey))
        val client = Uds27Client(ecu)

        val result = client.unlock()

        assertTrue("expected Denied, got $result", result is Uds27Client.Result.Denied)
        val denied = result as Uds27Client.Result.Denied
        assertEquals(0x35, denied.nrc)
        assertEquals("invalidKey", denied.message)
    }

    @Test
    fun lockedOut_propagatesNrc36OnFirstResponse() {
        val ecu = open(FakeEcuTransport(behavior = FakeEcuTransport.Behavior.LockedOut))
        val client = Uds27Client(ecu)

        val result = client.unlock()

        assertTrue("expected Denied, got $result", result is Uds27Client.Result.Denied)
        val denied = result as Uds27Client.Result.Denied
        assertEquals(0x36, denied.nrc)
        assertEquals("exceededNumberOfAttempts", denied.message)
        // Only RequestSeed was sent — we never got past the seed step.
        assertEquals(1, ecu.sent.size)
    }

    @Test
    fun silentEcu_returnsTransportError() {
        val ecu = open(FakeEcuTransport(behavior = FakeEcuTransport.Behavior.Silent))
        val client = Uds27Client(ecu, timeoutMs = 50)

        val result = client.unlock()

        assertTrue("expected TransportError, got $result", result is Uds27Client.Result.TransportError)
    }
}
