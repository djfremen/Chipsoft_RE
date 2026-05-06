package com.example.chipsoft_tech2

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.chipsoft_tech2.uds.CanFrame
import com.example.chipsoft_tech2.uds.CanTransport
import com.example.chipsoft_tech2.uds.UdsReadEcuInfoClient
import java.util.ArrayDeque

/**
 * Tech2-on-Chipsoft skeleton — first runnable screen.
 *
 * The screen wires [UdsReadEcuInfoClient] against an in-memory loopback
 * transport so the UDS plumbing is exercisable *before* a Chipsoft Pro
 * adapter is plugged in. Once a USB-CDC transport is implemented, swap
 * `LoopbackTransport(...)` for the real one and the same UI drives a real
 * SAAB ECM.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    HomeScreen()
                }
            }
        }
    }
}

@Composable
private fun HomeScreen() {
    var output by remember {
        mutableStateOf(
            "Tap a button to exercise the UDS layer.\n" +
                "Using in-memory loopback until the Chipsoft USB-CDC transport is wired.",
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Text(text = "Chipsoft Tech2", style = MaterialTheme.typography.headlineSmall)
        Text(
            text = "UDS-over-CAN client targeting the SAAB Trionic 8 ECM " +
                "via a Chipsoft J2534 Pro adapter (USB-CDC).",
            style = MaterialTheme.typography.bodyMedium,
        )

        HorizontalDivider()

        Button(modifier = Modifier.fillMaxWidth(), onClick = { output = run { read(UdsReadEcuInfoClient.Pid.EcuHardware) } }) {
            Text("Read PI 0x71 (ECU hardware)")
        }
        Button(modifier = Modifier.fillMaxWidth(), onClick = { output = read(UdsReadEcuInfoClient.Pid.Vin) }) {
            Text("Read PI 0x90 (VIN)")
        }
        Button(modifier = Modifier.fillMaxWidth(), onClick = { output = read(UdsReadEcuInfoClient.Pid.SubnetHsConfig) }) {
            Text("Read PI 0xB9 (subnet config HS)")
        }
        Button(modifier = Modifier.fillMaxWidth(), onClick = { output = readPid(0xFF) }) {
            Text("Read PI 0xFF (NRC test)")
        }

        HorizontalDivider()

        Text(text = output, style = MaterialTheme.typography.bodySmall)
    }
}

// === In-process loopback so the screen above runs before real hardware. ===

/**
 * Minimal echo-only transport. Implements [CanTransport] with a queue of
 * pre-baked responses keyed on the request bytes. Mirrors what
 * [com.example.chipsoft_tech2.uds.UdsReadEcuInfoClient] needs without the
 * SecurityAccess machinery the test fake carries.
 */
private class LoopbackTransport(
    private val ecuIdData: Map<Int, ByteArray>,
    private val requestId: Int = 0x7E0,
    private val responseId: Int = 0x7E8,
) : CanTransport {
    private val outbox = ArrayDeque<CanFrame>()
    private val pendingCFs = ArrayDeque<CanFrame>()
    private var open = false

    override fun open(bitrate: Int) { open = true }
    override fun close() { open = false; outbox.clear(); pendingCFs.clear() }

    override fun send(frame: CanFrame) {
        check(open) { "transport not open" }
        if (frame.id != requestId) return
        val data = frame.data
        when {
            data[0] == 0x02.toByte() && data[1] == 0x1A.toByte() -> handleReadEcuId(data[2].toInt() and 0xFF)
            data[0] == 0x30.toByte() -> { outbox.addAll(pendingCFs); pendingCFs.clear() }
        }
    }

    override fun receive(idFilter: Int?, timeoutMs: Int): CanFrame? {
        val frame = outbox.poll() ?: return null
        if (idFilter != null && frame.id != idFilter) return null
        return frame
    }

    private fun handleReadEcuId(pid: Int) {
        val payload = ecuIdData[pid]
        if (payload == null) {
            reply(byteArrayOf(0x03, 0x7F, 0x1A, 0x31)); return       // requestOutOfRange
        }
        val udsLen = 2 + payload.size                                 // 5A + PID + payload
        if (udsLen <= 7) {
            val frame = ByteArray(8)
            frame[0] = udsLen.toByte()
            frame[1] = 0x5A; frame[2] = pid.toByte()
            payload.copyInto(frame, 3)
            outbox.add(CanFrame(responseId, frame))
            return
        }
        // Multi-frame: FF + CFs.
        val ff = ByteArray(8)
        ff[0] = (0x10 or ((udsLen ushr 8) and 0x0F)).toByte()
        ff[1] = (udsLen and 0xFF).toByte()
        ff[2] = 0x5A; ff[3] = pid.toByte()
        val firstChunk = minOf(4, payload.size)
        payload.copyInto(ff, 4, 0, firstChunk)
        outbox.add(CanFrame(responseId, ff))

        var written = firstChunk
        var sn = 1
        while (written < payload.size) {
            val cf = ByteArray(8)
            cf[0] = (0x20 or (sn and 0x0F)).toByte()
            val take = minOf(7, payload.size - written)
            payload.copyInto(cf, 1, written, written + take)
            pendingCFs.add(CanFrame(responseId, cf))
            written += take; sn++
        }
    }

    private fun reply(udsBody: ByteArray) {
        val padded = ByteArray(8)
        udsBody.copyInto(padded)
        outbox.add(CanFrame(responseId, padded))
    }
}

private fun newClient(): UdsReadEcuInfoClient {
    val ecu = LoopbackTransport(
        ecuIdData = mapOf(
            0x71 to "5165290".toByteArray(),                    // ECU hardware part number
            0x90 to "YS3FD49Y541012017".toByteArray(),          // captured-fixture VIN
            0xB9 to byteArrayOf(0x12, 0x34),                    // subnet config bytes
        ),
    ).also { it.open(500_000) }
    return UdsReadEcuInfoClient(ecu)
}

private fun read(pid: UdsReadEcuInfoClient.Pid): String =
    format("PI 0x%02X".format(pid.code), newClient().read(pid))

private fun readPid(pid: Int): String =
    format("PI 0x%02X".format(pid), newClient().readPid(pid, asciiHint = false))

private fun format(label: String, result: UdsReadEcuInfoClient.Result): String = when (result) {
    is UdsReadEcuInfoClient.Result.Ascii ->
        "$label → ASCII \"${result.text}\"  (${result.raw.size} bytes raw)"
    is UdsReadEcuInfoClient.Result.Bytes ->
        "$label → ${result.bytes.joinToString(" ") { "%02X".format(it) }}  (${result.bytes.size} bytes)"
    is UdsReadEcuInfoClient.Result.NegativeResponse ->
        "$label → NRC 0x%02X  (%s)".format(result.nrc, result.message)
    is UdsReadEcuInfoClient.Result.TransportError ->
        "$label → transport error: ${result.message}"
}
