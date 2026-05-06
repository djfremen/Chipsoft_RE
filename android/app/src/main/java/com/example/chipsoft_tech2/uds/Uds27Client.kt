package com.example.chipsoft_tech2.uds

import com.example.chipsoft_tech2.crypto.SaabSeedToKey

/**
 * UDS service 0x27 (SecurityAccess) client for SAAB Trionic 8.
 *
 * Wire sequence (single ISO-TP frames, 11-bit IDs):
 *
 *   TX 0x7E0 → 02 27 LL 00 00 00 00 00      (RequestSeed, level LL)
 *   RX 0x7E8 ← 04 67 LL S1 S2 00 00 00      (Seed = S1 S2)
 *
 *   key = SaabSeedToKey.calcT8(seed, level)
 *
 *   TX 0x7E0 → 04 27 LL+1 K1 K2 00 00 00    (SendKey)
 *   RX 0x7E8 ← 02 67 LL+1 00 00 00 00 00    (Granted)
 *      or:    03 7F 27 NRC 00 00 00 00      (Denied; NRC = error code)
 *
 * Reference: mattiasclaesson/Trionic — TrionicCANLib/Trionic8.cs:310-419.
 *
 * @param transport an open [CanTransport] (caller is responsible for open/close)
 * @param requestId 0x7E0 by default (SAAB engine ECM). Override for other modules.
 * @param responseId 0x7E8 by default.
 * @param timeoutMs P2-server time per ISO 14229; SAAB Tech2 uses ~2000 ms.
 */
class Uds27Client(
    private val transport: CanTransport,
    private val requestId: Int = 0x7E0,
    private val responseId: Int = 0x7E8,
    private val timeoutMs: Int = 2000,
) {

    sealed class Result {
        object Granted : Result()
        data class AlreadyGranted(val why: String = "seed was 00 00") : Result()
        data class Denied(val nrc: Int, val message: String) : Result()
        data class TransportError(val message: String) : Result()
    }

    /**
     * Perform the full RequestSeed → SeedToKey → SendKey handshake at [level].
     * Default is L01 — the engine-ECM path used by Tech2Win for normal access.
     */
    fun unlock(level: SaabSeedToKey.T8Level = SaabSeedToKey.T8Level.L01): Result {
        val levelByte = level.code.toByte()

        // 1. RequestSeed
        send(byteArrayOf(0x02, 0x27, levelByte))
        val seedFrame = receiveOrFail() ?: return Result.TransportError("no response to RequestSeed")
        val seedRsp = seedFrame.data
        if (seedRsp.size < 5) {
            return Result.TransportError("seed response too short: ${seedRsp.size} bytes")
        }
        // Negative response shape: 03 7F 27 NRC ...
        if (seedRsp[1] == 0x7F.toByte() && seedRsp[2] == 0x27.toByte()) {
            val nrc = seedRsp[3].toInt() and 0xFF
            return Result.Denied(nrc, nrcText(nrc))
        }
        // Positive response: 04 67 LL SH SL
        if (seedRsp[1] != 0x67.toByte() || seedRsp[2] != levelByte) {
            return Result.TransportError(
                "unexpected RequestSeed response: ${seedRsp.toHex()}"
            )
        }
        val seedHi = seedRsp[3]
        val seedLo = seedRsp[4]
        val seed = SaabSeedToKey.seedFromBytes(seedHi, seedLo)
        if (seed == 0) {
            return Result.AlreadyGranted()
        }

        // 2. Compute key + SendKey
        val key = SaabSeedToKey.calcT8(seed, level)
        val keyBytes = SaabSeedToKey.keyToBytes(key)
        val sendKeySub = (level.code + 1).toByte()    // L01 → 0x02, LFB → 0xFC, LFD → 0xFE
        send(byteArrayOf(0x04, 0x27, sendKeySub, keyBytes[0], keyBytes[1]))

        val ackFrame = receiveOrFail() ?: return Result.TransportError("no response to SendKey")
        val ackRsp = ackFrame.data
        if (ackRsp.size < 3) {
            return Result.TransportError("SendKey ack too short: ${ackRsp.size} bytes")
        }
        if (ackRsp[1] == 0x7F.toByte() && ackRsp[2] == 0x27.toByte()) {
            val nrc = ackRsp[3].toInt() and 0xFF
            return Result.Denied(nrc, nrcText(nrc))
        }
        if (ackRsp[1] == 0x67.toByte() && ackRsp[2] == sendKeySub) {
            return Result.Granted
        }
        return Result.TransportError("unexpected SendKey response: ${ackRsp.toHex()}")
    }

    /** Build an 8-byte ISO-TP single frame from the UDS payload and send it. */
    private fun send(udsPayload: ByteArray) {
        require(udsPayload.size <= 7) { "UDS payload ≤ 7 bytes for single-frame ISO-TP" }
        val frame = ByteArray(8)
        udsPayload.copyInto(frame)
        // The first byte of udsPayload is already the ISO-TP single-frame header
        // (high nibble 0 = SF, low nibble = length). Rest auto-zeros via ByteArray init.
        transport.send(CanFrame(requestId, frame))
    }

    private fun receiveOrFail(): CanFrame? = transport.receive(responseId, timeoutMs)

    /** Translate an NRC byte to its standard ISO 14229 meaning (subset).
     *  Reference: mattiasclaesson/Trionic — TrionicCANLib/KWP/KWPHandler.cs:1313 area. */
    private fun nrcText(nrc: Int): String = when (nrc) {
        0x10 -> "generalReject"
        0x11 -> "serviceNotSupported"
        0x12 -> "subFunctionNotSupported"
        0x22 -> "conditionsNotCorrect"
        0x24 -> "requestSequenceError"
        0x35 -> "invalidKey"
        0x36 -> "exceededNumberOfAttempts"
        0x37 -> "requiredTimeDelayNotExpired"
        0x78 -> "requestCorrectlyReceived-ResponsePending"
        else -> "0x%02X".format(nrc)
    }

    private fun ByteArray.toHex(): String = joinToString(" ") { "%02X".format(it) }
}
