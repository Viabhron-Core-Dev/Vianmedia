import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

# Remove updateOrientation from inside mainListener
old_func = """            private fun updateOrientation(videoSize: VideoSize) {
                if (videoSize.width > 0 && videoSize.height > 0) {
                    val isPortrait = if (videoSize.unappliedRotationDegrees % 180 == 0) {
                        videoSize.height > videoSize.width
                    } else {
                        videoSize.width > videoSize.height
                    }
                    context.findActivity()?.requestedOrientation = if (isPortrait) {
                        ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                    } else {
                        ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                    }
                }
            }"""

content = content.replace(old_func, "")

# Insert it before mainListener
insert_pos = "        val mainListener = object : androidx.media3.common.Player.Listener {"

new_func = """
        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
            if (videoSize.width > 0 && videoSize.height > 0) {
                val isPortrait = if (videoSize.unappliedRotationDegrees % 180 == 0) {
                    videoSize.height > videoSize.width
                } else {
                    videoSize.width > videoSize.height
                }
                context.findActivity()?.requestedOrientation = if (isPortrait) {
                    ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                } else {
                    ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                }
            }
        }
        val mainListener = object : androidx.media3.common.Player.Listener {"""

content = content.replace(insert_pos, new_func)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)

print("Fixed updateOrientation location")
