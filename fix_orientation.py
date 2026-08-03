with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

old_func = """        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
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

new_func = """        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
            if (videoSize.width > 0 && videoSize.height > 0) {
                @Suppress("DEPRECATION")
                val w = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.width else videoSize.height
                @Suppress("DEPRECATION")
                val h = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.height else videoSize.width
                val isPortrait = h > w
                settingsManager.saveVideoOrientation(decodedUriString, isPortrait)
                context.findActivity()?.requestedOrientation = if (isPortrait) {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                } else {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                }
            }
        }"""

content = content.replace(old_func, new_func)
with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
