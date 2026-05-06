package com.example.chipsoft_tech2.crypto

/**
 * SAAB seed→key derivation for UDS service 0x27 (SecurityAccess) over CAN.
 *
 * Ported from mattiasclaesson/Trionic — TrionicCANLib/SeedToKey.cs.
 * Validated against 45 captured (seed, key) pairs from real ECM-granted
 * unlocks spanning 2021-11-11 .. 2025-01-31. See Chipsoft_RE/notes/
 * 2026-05-05-algorithm-verified.md for the validation set.
 *
 * Distinct from [SecurityCalculator] in this package, which handles the
 * SSA bench-card rolling-key flow. This file is for live UDS 0x27
 * exchange with an ECM (Trionic 8 / ME96 / CIM).
 */
object SaabSeedToKey {

    enum class T8Level(val code: Int) {
        L01(0x01),
        LFB(0xFB),
        LFD(0xFD),
    }

    /** Trionic 8 (and Z22SE) SecurityAccess key for the given seed and access level. */
    fun calcT8(seed: Int, level: T8Level = T8Level.L01): Int {
        require(seed in 0..0xFFFF) { "seed must be 0..0xFFFF, got 0x${seed.toString(16)}" }
        var key = ((seed ushr 5) or (seed shl 11)) and 0xFFFF
        key = (key + 0xB988) and 0xFFFF
        when (level) {
            T8Level.L01 -> {}
            T8Level.LFB -> {
                key = key xor 0x8749
                key = (key + 0x06D3) and 0xFFFF
                key = key xor 0xCFDF
            }
            T8Level.LFD -> {
                key /= 3
                key = key xor 0x8749
                key = (key + 0x0ACF) and 0xFFFF
                key = key xor 0x81BF
            }
        }
        return key and 0xFFFF
    }

    /** CIM (Column Integration Module) SecurityAccess key. */
    fun calcCim(seed: Int): Int {
        require(seed in 0..0xFFFF) { "seed must be 0..0xFFFF, got 0x${seed.toString(16)}" }
        var key = (seed + 0x9130) and 0xFFFF
        key = ((key ushr 8) or (key shl 8)) and 0xFFFF        // byte-swap
        return (0x3FC7 - key) and 0xFFFF
    }

    /** Motronic 96 (ME96) SecurityAccess key. */
    fun calcMe96(seed: Int): Int {
        require(seed in 0..0xFFFF) { "seed must be 0..0xFFFF, got 0x${seed.toString(16)}" }
        var c2 = (0xEB + seed) and 0xFF
        if (seed in 0x3808..0xA407) {
            c2 -= 1
        }
        return ((c2 shl 9) or
                ((((0x5BF8 + seed) ushr 8) and 0xFF) shl 1) or
                ((c2 ushr 7) and 1)) and 0xFFFF
    }

    /** Convenience: split a 16-bit key into two big-endian bytes (K_hi, K_lo). */
    fun keyToBytes(key: Int): ByteArray = byteArrayOf(
        ((key ushr 8) and 0xFF).toByte(),
        (key and 0xFF).toByte(),
    )

    /** Convenience: assemble two big-endian bytes (S_hi, S_lo) into a 16-bit seed. */
    fun seedFromBytes(hi: Byte, lo: Byte): Int =
        ((hi.toInt() and 0xFF) shl 8) or (lo.toInt() and 0xFF)
}
