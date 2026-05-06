package com.example.chipsoft_tech2.uds

/**
 * A single CAN frame — minimal subset we need for UDS over CAN.
 *
 * For SAAB Trionic 8 SecurityAccess, every request and response is an
 * ISO-TP single frame (≤ 7 bytes payload) with 11-bit IDs:
 *   - request  : 0x7E0
 *   - response : 0x7E8
 *
 * 8-byte data field is the ISO-TP convention; SAE J1939 / 29-bit IDs
 * not needed for our path (extended = false always for Trionic 8).
 */
data class CanFrame(
    val id: Int,
    val data: ByteArray,
    val extended: Boolean = false,
) {
    init {
        require(data.size <= 8) { "CAN frame data must be ≤ 8 bytes, got ${data.size}" }
        require(id in 0..0x1FFFFFFF) { "CAN id out of range: 0x${id.toString(16)}" }
    }

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is CanFrame) return false
        return id == other.id && extended == other.extended && data.contentEquals(other.data)
    }

    override fun hashCode(): Int =
        (id * 31 + extended.hashCode()) * 31 + data.contentHashCode()

    override fun toString(): String =
        "CanFrame(id=0x${id.toString(16).uppercase()}, data=${data.joinToString(" ") { "%02X".format(it) }})"
}
