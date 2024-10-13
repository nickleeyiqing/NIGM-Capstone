package com.example.nigm

import android.content.Context
import android.hardware.camera2.CameraCaptureSession
import android.hardware.camera2.CameraDevice
import android.hardware.camera2.CameraManager
import android.view.Surface
import android.view.TextureView

class CameraPreview(private val context: Context, private val textureView: TextureView) {

    fun startCameraPreview() {
        val cameraManager = context.getSystemService(Context.CAMERA_SERVICE) as CameraManager
        val cameraId = cameraManager.cameraIdList[0]

        cameraManager.openCamera(cameraId, object : CameraDevice.StateCallback() {
            override fun onOpened(camera: CameraDevice) {
                val previewSurface = Surface(textureView.surfaceTexture)
                val previewRequest = camera.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW)
                previewRequest.addTarget(previewSurface)

                camera.createCaptureSession(listOf(previewSurface), object : CameraCaptureSession.StateCallback() {
                    override fun onConfigured(session: CameraCaptureSession) {
                        session.setRepeatingRequest(previewRequest.build(), null, null)
                    }

                    override fun onConfigureFailed(session: CameraCaptureSession) {
                        // Handle failure
                    }
                }, null)
            }

            override fun onDisconnected(camera: CameraDevice) {
                // Handle disconnection
            }

            override fun onError(camera: CameraDevice, error: Int) {
                // Handle errors
            }
        }, null)
    }
}
