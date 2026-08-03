import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

# We need to replace the LaunchedEffects to include setVideoEffects
launched_effects = """    LaunchedEffect(editState.rotateConfig, editState.cropRect, editState.cropLeft, editState.cropRight, editState.cropTop, editState.cropBottom, editState.aspectRatio, currentTool) {
        val effects = mutableListOf<androidx.media3.common.Effect>()
        
        if (editState.rotateConfig != 0) {
            effects.add(androidx.media3.effect.ScaleAndRotateTransformation.Builder().setRotationDegrees(editState.rotateConfig.toFloat()).build())
        }
        
        if (currentTool != VideoEditorTool.CROP) {
            if (editState.cropRect == "Custom") {
                val cw = editState.cropRight - editState.cropLeft
                val ch = editState.cropBottom - editState.cropTop
                if (cw > 0 && ch > 0) {
                    val left = editState.cropLeft * 2f - 1f
                    val right = editState.cropRight * 2f - 1f
                    val top = 1f - editState.cropTop * 2f
                    val bottom = 1f - editState.cropBottom * 2f
                    effects.add(androidx.media3.effect.Crop(left, right, bottom, top))
                }
            }
            
            if (editState.aspectRatio != "Original" && editState.aspectRatio != "Center Crop") {
                val ratioFloat = when (editState.aspectRatio) {
                    "16:9" -> 16f / 9f
                    "9:16" -> 9f / 16f
                    "1:1" -> 1f
                    "4:3" -> 4f / 3f
                    "21:9" -> 21f / 9f
                    else -> 1f
                }
                effects.add(androidx.media3.effect.Presentation.createForAspectRatio(ratioFloat, androidx.media3.effect.Presentation.LAYOUT_SCALE_TO_FIT_WITH_CROP))
            }
        }
        
        exoPlayer?.setVideoEffects(effects)
    }

    // Live preview updates based on edit state
    LaunchedEffect(editState.speed) {"""

content = re.sub(r'    // Live preview updates based on edit state\s+LaunchedEffect\(editState\.speed\) \{', launched_effects, content)

# Now, let's fix onVideoSizeChanged
old_on_video = """                    override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
                        if (videoSize.width > 0 && videoSize.height > 0) {
                            if (videoSize.unappliedRotationDegrees == 90 || videoSize.unappliedRotationDegrees == 270) {
                                videoWidth = videoSize.height
                                videoHeight = videoSize.width
                            } else {
                                videoWidth = videoSize.width
                                videoHeight = videoSize.height
                            }
                        }
                    }"""

new_on_video = """                    override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
                        if (videoSize.width > 0 && videoSize.height > 0) {
                            if (videoSize.unappliedRotationDegrees == 90 || videoSize.unappliedRotationDegrees == 270) {
                                videoWidth = videoSize.height
                                videoHeight = videoSize.width
                            } else {
                                videoWidth = videoSize.width
                                videoHeight = videoSize.height
                            }
                        }
                    }"""

# Wait, if ExoPlayer output has unappliedRotationDegrees=0, the existing logic `videoWidth = videoSize.width` works! So we don't even need to change onVideoSizeChanged!

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)
