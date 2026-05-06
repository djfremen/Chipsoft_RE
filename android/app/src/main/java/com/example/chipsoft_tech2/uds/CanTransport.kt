package com.example.chipsoft_tech2.uds

/**
 * Abstraction over a CAN bus link. Implementations:
 *
 *   - `SlcanTransport`  — Chipsoft Pro in CANHacker mode, lawicel ASCII over USB-CDC
 *   - `J2534Transport`  — Chipsoft Pro in J2534 mode, vendor wire envelope
 *                         (8-byte LE header + payload + sum16-checksum, see
 *                         Chipsoft_RE/notes/2026-05-05-ghidra-drain.md)
 *   - `FakeEcuTransport` — in-memory simulator for unit tests
 *
 * Both real transports are TODO until bench validation. The interface lets
 * us write [Uds27Client] and its tests today, and slot the real implementation
 * in once we know which one survives bench tests.
 */
interface CanTransport {

    /**
     * Open the link at the given bit rate.
     *
     * SAAB Trionic 8 engine ECM lives on SWCAN @ 33333 bps on OBD-II pin 1.
     * HSCAN modules typically @ 500000 bps on pins 6/14.
     */
    fun open(bitrate: Int)

    /** Close the link. Idempotent. */
    fun close()

    /** Write a single CAN frame to the bus. */
    fun send(frame: CanFrame)

    /**
     * Block (with timeout) for the next frame matching `idFilter`, or null
     * if the timeout elapses. Pass `null` for `idFilter` to receive any frame.
     */
    fun receive(idFilter: Int?, timeoutMs: Int): CanFrame?
}
