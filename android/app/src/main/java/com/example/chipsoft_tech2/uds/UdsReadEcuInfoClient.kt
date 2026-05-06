package com.example.chipsoft_tech2.uds

/**
 * UDS service 0x1A (ReadEcuIdentification) client for SAAB Trionic 8.
 *
 * Lifted from `mattiasclaesson/Trionic — TrionicCANLib/Trionic8.cs`:
 *   - `RequestECUInfo(uint pid)`            — binary read (line 787)
 *   - `RequestECUInfoAsString(uint pid)`    — ASCII read (lines 570-682)
 *
 * Wire shape:
 *
 *   TX 0x7E0 → 02 1A PP 00 00 00 00 00              (single frame request)
 *
 *   RX 0x7E8 ← LL 5A PP D1 D2 ...                   (single frame response)
 *      or
 *      ← 1L LL 5A PP D1 D2 D3 D4                    (first frame, 12-bit length)
 *      → 30 00 00 00 00 00 00 00                    (flow control: CTS, BS=0, ST=0)
 *      ← 21 D5 D6 D7 D8 D9 D10 D11                  (consecutive frame, sn=1)
 *      ← 22 D12 ...                                 (consecutive frame, sn=2)
 *      ...
 *
 *   Negative response: 03 7F 1A NRC ...
 *
 * No SecurityAccess required for Trionic 8 ReadEcuIdentification on the
 * standard PIDs — that's why this is a safe first call to start with.
 *
 * @param transport an open [CanTransport] (caller is responsible for open/close)
 * @param requestId 0x7E0 by default (SAAB engine ECM on HS-CAN). Override for other modules.
 * @param responseId 0x7E8 by default.
 * @param timeoutMs P2-server time per ISO 14229. SAAB uses ~2000 ms; up to 6000 ms after a
 *                  pending NRC (0x78).
 */
class UdsReadEcuInfoClient(
    private val transport: CanTransport,
    private val requestId: Int = 0x7E0,
    private val responseId: Int = 0x7E8,
    private val timeoutMs: Int = 2000,
) {

    /**
     * Trionic 8 ECU-identification PIDs from
     * `mattiasclaesson/Trionic — TrionicCANLib/Trionic8.cs:1189..1300`.
     *
     * The `String` flag indicates Trionic.NET interprets the response as ASCII;
     * binary PIDs (e.g. SubnetConfigHighSpeed) are returned raw.
     */
    enum class Pid(val code: Int, val ascii: Boolean, val description: String) {
        // ASCII identifiers — Trionic.NET parses as Encoding.ASCII
        BuildDate          (0x0A, true,  "Build date (BCD-style ASCII)"),
        EcuHardware        (0x71, true,  "ECU hardware part number"),
        EcuDescription     (0x72, true,  "ECU description"),
        CodefileVersion    (0x73, true,  "Codefile version"),
        CalibrationSet     (0x74, true,  "Calibration set"),
        SoftwareVersion    (0x08, true,  "Software version (raw)"),
        Vin                (0x90, true,  "Vehicle Identification Number (17 chars)"),
        EcuSwVersionNumber (0x95, true,  "ECU SW version number (DEALERPN-style)"),
        ProgrammingDate    (0x99, true,  "Programming date"),
        SerialNumber       (0xB4, true,  "ECU serial number"),

        // Binary identifiers — single-byte or fixed-shape responses
        DiagnosticAddress  (0xB0, false, "Diagnostic address (1 byte)"),
        BoschEnableCounter (0x70, false, "Bosch enable counter (1 byte)"),
        SubnetHsConfig     (0xB9, false, "Subnet config list HS — ECM/ABS/SADS/TCM/CIM (2 bytes)"),
        WheelCircumference (0x24, false, "Wheel circumference cm"),
        DiagnosticDataId   (0x9A, false, "Diagnostic data identifier"),
    }

    sealed class Result {
        /** Successful ASCII response. [text] is the trimmed payload (trailing NULs removed). */
        data class Ascii(val pid: Int, val text: String, val raw: ByteArray) : Result() {
            override fun equals(other: Any?): Boolean =
                other is Ascii && pid == other.pid && text == other.text && raw.contentEquals(other.raw)
            override fun hashCode(): Int = (pid * 31 + text.hashCode()) * 31 + raw.contentHashCode()
        }
        /** Successful binary response (raw bytes after the `5A PP` header). */
        data class Bytes(val pid: Int, val bytes: ByteArray) : Result() {
            override fun equals(other: Any?): Boolean =
                other is Bytes && pid == other.pid && bytes.contentEquals(other.bytes)
            override fun hashCode(): Int = pid * 31 + bytes.contentHashCode()
        }
        /** ECU returned `7F 1A NRC`. */
        data class NegativeResponse(val pid: Int, val nrc: Int, val message: String) : Result()
        /** Frame parsing or transport error (timeout, malformed, mismatched PID). */
        data class TransportError(val message: String) : Result()
    }

    /**
     * Convenience: read a known [Pid] enum entry. The ASCII vs binary
     * interpretation follows the [Pid.ascii] flag; pass `forceAscii = true` to
     * always decode as ASCII regardless.
     */
    fun read(pid: Pid, forceAscii: Boolean = false): Result =
        readPid(pid.code, asciiHint = forceAscii || pid.ascii)

    /**
     * Read an arbitrary 1-byte PID. [asciiHint] controls how the payload is
     * presented; defaults to binary ([Result.Bytes]).
     */
    fun readPid(pid: Int, asciiHint: Boolean = false): Result {
        require(pid in 0..0xFF) { "PID must fit in one byte: 0x${pid.toString(16)}" }

        send(byteArrayOf(0x02, 0x1A, pid.toByte()))
        val first = receiveOrFail()
            ?: return Result.TransportError("no response to ReadEcuId(0x%02X)".format(pid))
        val rsp = first.data
        if (rsp.size < 4) {
            return Result.TransportError("response too short: ${rsp.size} bytes ${rsp.toHex()}")
        }

        // Negative response: SF nibble 0, length 3, then 7F 1A NRC.
        // Two shapes are tolerant: 03 7F 1A NRC ... or [SF byte][7F 1A NRC ...] depending on padding.
        if (rsp[1] == 0x7F.toByte() && rsp[2] == 0x1A.toByte()) {
            val nrc = rsp[3].toInt() and 0xFF
            // 0x78 = response pending — wait once more with a longer timeout
            if (nrc == 0x78) {
                val retry = transport.receive(responseId, timeoutMs * 3)
                    ?: return Result.NegativeResponse(pid, 0x78, nrcText(0x78))
                return parseRsp(pid, retry.data, asciiHint)
            }
            return Result.NegativeResponse(pid, nrc, nrcText(nrc))
        }

        return parseRsp(pid, rsp, asciiHint)
    }

    private fun parseRsp(pid: Int, rsp: ByteArray, asciiHint: Boolean): Result {
        val frameType = rsp[0].toInt() and 0xF0
        return when (frameType) {
            0x00 -> parseSingleFrame(pid, rsp, asciiHint)
            0x10 -> parseFirstFrame(pid, rsp, asciiHint)
            else -> Result.TransportError(
                "unknown ISO-TP frame type 0x%02X in %s".format(rsp[0].toInt() and 0xFF, rsp.toHex())
            )
        }
    }

    /** Single frame: byte 0 high nibble = 0, low nibble = UDS length (max 7). */
    private fun parseSingleFrame(pid: Int, rsp: ByteArray, asciiHint: Boolean): Result {
        val sfLen = rsp[0].toInt() and 0x0F
        if (sfLen < 2 || sfLen > 7) {
            return Result.TransportError("bad SF length $sfLen in ${rsp.toHex()}")
        }
        if (rsp.size < sfLen + 1) {
            return Result.TransportError("SF truncated: claims $sfLen UDS bytes, frame has ${rsp.size}")
        }
        if (rsp[1] != 0x5A.toByte()) {
            return Result.TransportError("expected positive response 0x5A, got 0x%02X".format(rsp[1]))
        }
        if (rsp[2] != pid.toByte()) {
            return Result.TransportError(
                "PID echo mismatch: requested 0x%02X, got 0x%02X".format(pid, rsp[2].toInt() and 0xFF)
            )
        }
        // Payload: [3 .. sfLen] inclusive. UDS bytes are at positions 1..sfLen.
        val payload = rsp.copyOfRange(3, sfLen + 1)
        return present(pid, payload, asciiHint)
    }

    /**
     * First frame of an ISO-TP segmented response.
     * Byte layout: `1L LL 5A PP D1 D2 D3 D4` where total UDS length = (high_nibble << 8) | byte[1].
     * Trionic 8 responses fit comfortably in one byte of length, but we honour the 12-bit field.
     */
    private fun parseFirstFrame(pid: Int, rsp: ByteArray, asciiHint: Boolean): Result {
        if (rsp.size < 8) return Result.TransportError("FF too short: ${rsp.size}")
        val totalLen = ((rsp[0].toInt() and 0x0F) shl 8) or (rsp[1].toInt() and 0xFF)
        if (totalLen < 3) return Result.TransportError("FF totalLen $totalLen too small")
        if (rsp[2] != 0x5A.toByte()) {
            return Result.TransportError("FF: expected 0x5A at byte 2, got 0x%02X".format(rsp[2]))
        }
        if (rsp[3] != pid.toByte()) {
            return Result.TransportError(
                "FF: PID echo mismatch: requested 0x%02X, got 0x%02X".format(pid, rsp[3].toInt() and 0xFF)
            )
        }
        val payloadSize = totalLen - 2  // strip 5A + PID
        val payload = ByteArray(payloadSize)
        // FF carries 4 payload bytes (frame bytes 4..7).
        val firstChunk = minOf(4, payloadSize)
        System.arraycopy(rsp, 4, payload, 0, firstChunk)
        var written = firstChunk

        sendFlowControl()

        var expectedSn = 1
        while (written < payloadSize) {
            val cf = receiveOrFail()
                ?: return Result.TransportError("CF timeout at $written/$payloadSize")
            val cfData = cf.data
            if (cfData.isEmpty()) return Result.TransportError("empty CF")
            val cfHigh = cfData[0].toInt() and 0xF0
            if (cfHigh != 0x20) {
                return Result.TransportError(
                    "expected CF (high nibble 2), got 0x%02X".format(cfData[0].toInt() and 0xFF)
                )
            }
            val sn = cfData[0].toInt() and 0x0F
            if (sn != (expectedSn and 0x0F)) {
                return Result.TransportError("CF sequence: expected $expectedSn, got $sn")
            }
            val take = minOf(7, payloadSize - written, cfData.size - 1)
            System.arraycopy(cfData, 1, payload, written, take)
            written += take
            expectedSn++
        }

        return present(pid, payload, asciiHint)
    }

    /** Wrap the parsed payload in an [Result.Ascii] or [Result.Bytes] based on hint. */
    private fun present(pid: Int, payload: ByteArray, asciiHint: Boolean): Result {
        if (!asciiHint) return Result.Bytes(pid, payload)
        // Strip trailing NULs so VIN-style responses don't show garbage.
        var end = payload.size
        while (end > 0 && payload[end - 1] == 0.toByte()) end--
        val text = String(payload, 0, end, Charsets.ISO_8859_1)
        return Result.Ascii(pid, text, payload)
    }

    /** ISO-TP single frame: 8 bytes, byte 0 = 0x0L (L = UDS payload length). */
    private fun send(udsPayload: ByteArray) {
        require(udsPayload.size in 1..7) { "UDS payload must be 1..7 bytes" }
        val frame = ByteArray(8)
        udsPayload.copyInto(frame)
        transport.send(CanFrame(requestId, frame))
    }

    /** Continue To Send, BS=0 (unlimited), ST=0 (no separation time). */
    private fun sendFlowControl() {
        val fc = ByteArray(8)
        fc[0] = 0x30.toByte()
        transport.send(CanFrame(requestId, fc))
    }

    private fun receiveOrFail(): CanFrame? = transport.receive(responseId, timeoutMs)

    /** ISO 14229 NRC subset relevant to ReadEcuIdentification. */
    private fun nrcText(nrc: Int): String = when (nrc) {
        0x10 -> "generalReject"
        0x11 -> "serviceNotSupported"
        0x12 -> "subFunctionNotSupported"
        0x13 -> "incorrectMessageLengthOrInvalidFormat"
        0x22 -> "conditionsNotCorrect"
        0x31 -> "requestOutOfRange"
        0x33 -> "securityAccessDenied"
        0x78 -> "requestCorrectlyReceived-ResponsePending"
        else -> "0x%02X".format(nrc)
    }

    private fun ByteArray.toHex(): String = joinToString(" ") { "%02X".format(it) }
}
