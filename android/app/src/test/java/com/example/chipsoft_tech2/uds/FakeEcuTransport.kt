package com.example.chipsoft_tech2.uds

import com.example.chipsoft_tech2.crypto.SaabSeedToKey
import java.util.ArrayDeque

/**
 * In-memory simulator of a SAAB Trionic 8 ECM responding to UDS 0x27.
 *
 * Configurable behaviors for testing different paths:
 *   - happy path: valid seed → expects correct key → grants
 *   - already-granted: returns seed `0x00 0x00`
 *   - bad key: returns NRC 0x35 (invalidKey) on SendKey
 *   - locked-out: returns NRC 0x36 (exceededNumberOfAttempts) immediately
 *   - silent: drops frames (test transport timeout handling)
 */
class FakeEcuTransport(
    private val seed: Int = 0x7F14,           // captured-fixture seed
    private val behavior: Behavior = Behavior.HappyPath,
    private val requestId: Int = 0x7E0,
    private val responseId: Int = 0x7E8,
    /**
     * Mock ECU-identification database keyed by 1-byte PID. Used by
     * [UdsReadEcuInfoClient] tests. When a request arrives for a PID not in
     * this map, the fake replies `7F 1A 31` (requestOutOfRange).
     */
    private val ecuIdData: Map<Int, ByteArray> = emptyMap(),
) : CanTransport {

    enum class Behavior {
        HappyPath, AlreadyGranted, BadKey, LockedOut, Silent,
    }

    private val outbox = ArrayDeque<CanFrame>()
    val sent = mutableListOf<CanFrame>()
    private var open = false

    /** Pending ISO-TP segmented send: when the client emits a flow-control frame,
     *  drain remaining consecutive frames from this queue. */
    private val pendingCFs = ArrayDeque<CanFrame>()

    override fun open(bitrate: Int) { open = true }
    override fun close() { open = false; outbox.clear(); pendingCFs.clear() }

    override fun send(frame: CanFrame) {
        check(open) { "transport not open" }
        check(frame.id == requestId) { "unexpected request id 0x${frame.id.toString(16)}" }
        sent += frame
        if (behavior == Behavior.Silent) return

        val data = frame.data
        when {
            // RequestSeed: 02 27 LL ...
            data[0] == 0x02.toByte() && data[1] == 0x27.toByte() -> handleRequestSeed(data[2])
            // SendKey: 04 27 LL+1 K1 K2
            data[0] == 0x04.toByte() && data[1] == 0x27.toByte() -> handleSendKey(data[2], data[3], data[4])
            // ReadEcuIdentification: 02 1A PP ...
            data[0] == 0x02.toByte() && data[1] == 0x1A.toByte() -> handleReadEcuId(data[2].toInt() and 0xFF)
            // Flow control (CTS): 30 BS ST — release any queued consecutive frames
            data[0] == 0x30.toByte() -> outbox.addAll(pendingCFs).also { pendingCFs.clear() }
        }
    }

    override fun receive(idFilter: Int?, timeoutMs: Int): CanFrame? {
        val frame = outbox.poll() ?: return null
        if (idFilter != null && frame.id != idFilter) return null
        return frame
    }

    private fun handleRequestSeed(level: Byte) {
        when (behavior) {
            Behavior.LockedOut -> reply(byteArrayOf(0x03, 0x7F, 0x27, 0x36))
            Behavior.AlreadyGranted -> reply(byteArrayOf(0x04, 0x67, level, 0, 0))
            else -> {
                val sh = ((seed ushr 8) and 0xFF).toByte()
                val sl = (seed and 0xFF).toByte()
                reply(byteArrayOf(0x04, 0x67, level, sh, sl))
            }
        }
    }

    private fun handleSendKey(sendKeySub: Byte, k1: Byte, k2: Byte) {
        val level = SaabSeedToKey.T8Level.values().firstOrNull { (it.code + 1).toByte() == sendKeySub }
            ?: SaabSeedToKey.T8Level.L01
        val expected = SaabSeedToKey.calcT8(seed, level)
        val expectedHi = ((expected ushr 8) and 0xFF).toByte()
        val expectedLo = (expected and 0xFF).toByte()
        val keyOk = (k1 == expectedHi && k2 == expectedLo)

        if (behavior == Behavior.BadKey || !keyOk) {
            reply(byteArrayOf(0x03, 0x7F, 0x27, 0x35))
        } else {
            reply(byteArrayOf(0x02, 0x67, sendKeySub))
        }
    }

    private fun reply(udsBody: ByteArray) {
        val padded = ByteArray(8)
        udsBody.copyInto(padded)
        outbox.add(CanFrame(responseId, padded))
    }

    private fun handleReadEcuId(pid: Int) {
        val payload = ecuIdData[pid]
        if (payload == null) {
            reply(byteArrayOf(0x03, 0x7F, 0x1A, 0x31))      // requestOutOfRange
            return
        }
        // UDS positive response = 5A PP D1 D2 ...   (length = 2 + payload.size)
        val udsLen = 2 + payload.size
        if (udsLen <= 7) {
            // Single frame: SF length nibble = udsLen, then 5A PP payload, padded.
            val frame = ByteArray(8)
            frame[0] = udsLen.toByte()
            frame[1] = 0x5A
            frame[2] = pid.toByte()
            payload.copyInto(frame, 3)
            outbox.add(CanFrame(responseId, frame))
            return
        }
        // Multi-frame: first frame carries 4 payload bytes; CFs each carry 7.
        // FF byte 0 high nibble = 1, low nibble + byte 1 = 12-bit total length.
        val ff = ByteArray(8)
        ff[0] = (0x10 or ((udsLen ushr 8) and 0x0F)).toByte()
        ff[1] = (udsLen and 0xFF).toByte()
        ff[2] = 0x5A
        ff[3] = pid.toByte()
        val firstChunk = minOf(4, payload.size)
        payload.copyInto(ff, 4, 0, firstChunk)
        outbox.add(CanFrame(responseId, ff))

        // Stage consecutive frames; they release when the client sends FC (0x30).
        var written = firstChunk
        var sn = 1
        while (written < payload.size) {
            val cf = ByteArray(8)
            cf[0] = (0x20 or (sn and 0x0F)).toByte()
            val take = minOf(7, payload.size - written)
            payload.copyInto(cf, 1, written, written + take)
            pendingCFs.add(CanFrame(responseId, cf))
            written += take
            sn++
        }
    }
}
