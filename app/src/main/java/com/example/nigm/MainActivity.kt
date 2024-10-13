package com.example.nigm

import android.Manifest
import android.app.Activity
import android.content.pm.PackageManager
import android.hardware.Camera
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.SurfaceHolder
import android.view.SurfaceView
import android.widget.Button
import android.widget.TextView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : Activity(), SurfaceHolder.Callback {

    private lateinit var surfaceView: SurfaceView
    private var camera: Camera? = null
    private var isMeasuring = false
    private val redChannelValues = mutableListOf<Int>()
    private lateinit var startButton: Button
    private lateinit var heartRateText: TextView
    private val samplingDuration = 10_000L // 10 seconds for sampling heart rate
    private val handler = Handler(Looper.getMainLooper()) // Handler for main thread

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        surfaceView = findViewById(R.id.surfaceView)
        startButton = findViewById(R.id.startButton)
        heartRateText = findViewById(R.id.heartRateText)

        surfaceView.holder.addCallback(this)

        startButton.setOnClickListener {
            if (isMeasuring) {
                stopHeartRateMeasurement()
            } else {
                startHeartRateMeasurement()
            }
        }

        // Check camera permission
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 50)
        }
    }

    private fun startHeartRateMeasurement() {
        camera?.let {
            val params = it.parameters
            params.flashMode = Camera.Parameters.FLASH_MODE_TORCH
            it.parameters = params
            isMeasuring = true
            startButton.text = "Stop Measuring"

            // Start collecting red channel data
            redChannelValues.clear()

            // Start handler for 10-second sampling
            handler.postDelayed({
                stopHeartRateMeasurement() // Stop measurement after 10 seconds
            }, samplingDuration)
        }
    }

    private fun stopHeartRateMeasurement() {
        camera?.let {
            val params = it.parameters
            params.flashMode = Camera.Parameters.FLASH_MODE_OFF
            it.parameters = params
            isMeasuring = false
            startButton.text = "Start Measuring"

            // Calculate heart rate and update the UI on the main thread
            val heartRate = calculateHeartRate(redChannelValues)
            runOnUiThread {
                heartRateText.text = "Heart Rate: $heartRate BPM" // This is the part that needs to run on the main thread
            }

            // Clear the collected red channel data
            redChannelValues.clear()
        }
    }

    private fun calculateHeartRate(redChannelValues: List<Int>): Int {
        if (redChannelValues.isEmpty()) return 0

        // Detect peaks from red channel values
        val peaks = detectPeaks(redChannelValues)

        if (peaks.isEmpty()) return 0 // No peaks found, unable to calculate heart rate

        // Calculate the average time between peaks
        val timeBetweenPeaks = samplingDuration.toFloat() / peaks.size

        // Calculate BPM (beats per minute)
        val bpm = (60_000f / timeBetweenPeaks).toInt() // 60,000 ms = 1 minute
        return bpm
    }

    private fun detectPeaks(data: List<Int>): List<Int> {
        val peaks = mutableListOf<Int>()

        for (i in 1 until data.size - 1) {
            if (data[i] > data[i - 1] && data[i] > data[i + 1]) {
                peaks.add(data[i])
            }
        }

        return peaks
    }

    override fun surfaceCreated(holder: SurfaceHolder) {
        try {
            camera = Camera.open().apply {
                setPreviewDisplay(holder)
                setPreviewCallback { data, camera ->
                    if (isMeasuring) {
                        val size = camera.parameters.previewSize
                        val rgb = decodeYUV420SPtoRGB(data, size.width, size.height)
                        val redValue = calculateRedChannel(rgb)
                        redChannelValues.add(redValue)
                    }
                }
                startPreview()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun calculateRedChannel(rgb: IntArray): Int {
        var redSum = 0
        for (pixel in rgb) {
            redSum += (pixel shr 16) and 0xFF // Extract red channel
        }
        return redSum / rgb.size
    }

    private fun decodeYUV420SPtoRGB(yuv420sp: ByteArray, width: Int, height: Int): IntArray {
        val frameSize = width * height
        val rgb = IntArray(frameSize)
        var uvp: Int
        var u: Int
        var v: Int
        for (j in 0 until height) {
            uvp = frameSize + (j shr 1) * width
            u = 0
            v = 0
            for (i in 0 until width) {
                val yp = j * width + i
                var y = (0xff and yuv420sp[yp].toInt()) - 16
                if (y < 0) y = 0
                if (i and 1 == 0) {
                    v = (0xff and yuv420sp[uvp++].toInt()) - 128
                    u = (0xff and yuv420sp[uvp++].toInt()) - 128
                }
                val y1192 = 1192 * y
                val r = (y1192 + 1634 * v).coerceIn(0, 262143)
                rgb[yp] = r shl 16
            }
        }
        return rgb
    }

    override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {}

    override fun surfaceDestroyed(holder: SurfaceHolder) {
        camera?.release()
        camera = null
    }
}
