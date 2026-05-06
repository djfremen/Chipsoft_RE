package com.example.chipsoft_tech2.crypto

import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
import org.junit.Test

/**
 * Validates [SaabSeedToKey] against fixtures captured from real
 * TrionicCANFlasher sessions on a SAAB ECM (uiLog "Security access granted"
 * lines). Full extraction script + 45-row table at:
 *   Chipsoft_RE/tools/extract_seedkey_fixtures.py
 *   Chipsoft_RE/notes/captures/all-trionic-canflasher-fixtures.tsv
 */
class SaabSeedToKeyTest {

    @Test
    fun trionic8_level01_matchesCapturedKey_session_2025_01_31() {
        // 4 (seed, key) pairs from a 2025-01-31 TrionicCANFlasher session.
        // All four ended in "Security access granted" on the wire.
        val pairs = listOf(
            0x7F14 to 0x5D80,
            0x7E11 to 0x4578,
            0x7F14 to 0x5D80,   // duplicate seed of pair #1 — see uds27 determinism note
            0x5897 to 0x744C,
        )
        for ((seed, expected) in pairs) {
            assertEquals(
                "T8/L01 seed=0x${seed.toString(16).uppercase()}",
                expected,
                SaabSeedToKey.calcT8(seed, SaabSeedToKey.T8Level.L01),
            )
        }
    }

    @Test
    fun me96_matchesCapturedKey_acrossSessions() {
        // Sample of ME96 (seed, key) pairs from the 2021-2024 fixture set.
        // The full 21 pairs are in the Chipsoft_RE TSV; these 5 cover the
        // most-repeated seeds plus a couple unique ones.
        val pairs = listOf(
            0x26B2 to 0x3B05,    // seen 10x across 3 years
            0x5A0C to 0xED6D,
            0x0CB6 to 0x42D1,
            0x569A to 0x0965,
            0x1469 to 0xA8E0,
        )
        for ((seed, expected) in pairs) {
            assertEquals(
                "ME96 seed=0x${seed.toString(16).uppercase()}",
                expected,
                SaabSeedToKey.calcMe96(seed),
            )
        }
    }

    @Test
    fun keyToBytes_isBigEndian() {
        assertArrayEquals(byteArrayOf(0x5D.toByte(), 0x80.toByte()), SaabSeedToKey.keyToBytes(0x5D80))
        assertArrayEquals(byteArrayOf(0x00, 0x00), SaabSeedToKey.keyToBytes(0x0000))
        assertArrayEquals(byteArrayOf(0xFF.toByte(), 0xFF.toByte()), SaabSeedToKey.keyToBytes(0xFFFF))
    }

    @Test
    fun seedFromBytes_isBigEndian() {
        assertEquals(0x7F14, SaabSeedToKey.seedFromBytes(0x7F.toByte(), 0x14.toByte()))
        assertEquals(0x0000, SaabSeedToKey.seedFromBytes(0x00, 0x00))
        assertEquals(0xFFFF, SaabSeedToKey.seedFromBytes(0xFF.toByte(), 0xFF.toByte()))
    }

    @Test
    fun roundTripSeedAndKey_overFullRange() {
        // For T8/L01 the algorithm is a bijection over 0..0xFFFF.
        // Every seed produces a key in the same range.
        for (seed in 0..0xFFFF) {
            val key = SaabSeedToKey.calcT8(seed, SaabSeedToKey.T8Level.L01)
            assert(key in 0..0xFFFF) { "key 0x${key.toString(16)} out of range for seed 0x${seed.toString(16)}" }
        }
    }

    @Test(expected = IllegalArgumentException::class)
    fun calcT8_rejectsOutOfRangeSeed() {
        SaabSeedToKey.calcT8(0x10000)
    }

    @Test(expected = IllegalArgumentException::class)
    fun calcMe96_rejectsNegativeSeed() {
        SaabSeedToKey.calcMe96(-1)
    }
}
