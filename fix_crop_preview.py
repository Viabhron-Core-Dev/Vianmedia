import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

old_effects = """        if (currentTool != VideoEditorTool.CROP) {
            if (editState.cropRect == "Center Crop") {
                effects.add(androidx.media3.effect.Presentation.createForAspectRatio(1f, androidx.media3.effect.Presentation.LAYOUT_SCALE_TO_FIT_WITH_CROP))
            } else if (editState.cropRect == "Custom") {
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
            
            if (editState.aspectRatio != "Original" && editState.cropRect != "Center Crop") {
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
        }"""

new_effects = """        if (editState.cropRect == "Center Crop") {
            effects.add(androidx.media3.effect.Presentation.createForAspectRatio(1f, androidx.media3.effect.Presentation.LAYOUT_SCALE_TO_FIT_WITH_CROP))
        } else if (editState.cropRect == "Custom" && currentTool != VideoEditorTool.CROP) {
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
        
        if (currentTool != VideoEditorTool.CROP) {
            if (editState.aspectRatio != "Original" && editState.cropRect != "Center Crop") {
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
        }"""

content = content.replace(old_effects, new_effects)

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)
