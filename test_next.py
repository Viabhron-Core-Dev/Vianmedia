import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

# Replace the updateOrientation logic
old_func = """        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
            if (videoSize.width > 0 && videoSize.height > 0) {
                val isPortrait = if (videoSize.unappliedRotationDegrees % 180 == 0) {
                    videoSize.height > videoSize.width
                } else {
                    videoSize.width > videoSize.height
                }
                settingsManager.saveVideoOrientation(decodedUriString, isPortrait)
                context.findActivity()?.requestedOrientation = if (isPortrait) {
                    ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                } else {
                    ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                }
            }
        }"""

new_func = """        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
            if (videoSize.width > 0 && videoSize.height > 0) {
                val isPortrait = videoSize.height > videoSize.width
                settingsManager.saveVideoOrientation(decodedUriString, isPortrait)
                context.findActivity()?.requestedOrientation = if (isPortrait) {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                } else {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                }
            }
        }"""

content = content.replace(old_func, new_func)

# Also add the else branch for savedOrientation
old_saved = """        val savedOrientation = settingsManager.getVideoOrientation(decodedUriString)
        if (savedOrientation != null) {
            context.findActivity()?.requestedOrientation = if (savedOrientation) {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            } else {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            }
        }"""

new_saved = """        val savedOrientation = settingsManager.getVideoOrientation(decodedUriString)
        if (savedOrientation != null) {
            context.findActivity()?.requestedOrientation = if (savedOrientation) {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            } else {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            }
        } else {
            context.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
        }"""

content = content.replace(old_saved, new_saved)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
