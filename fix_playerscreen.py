import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

# Add read orientation logic and fix updateOrientation
old_func = """        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
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

new_func = """        val savedOrientation = settingsManager.getVideoOrientation(decodedUriString)
        if (savedOrientation != null) {
            context.findActivity()?.requestedOrientation = if (savedOrientation) {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            } else {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            }
        }

        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
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

content = content.replace(old_func, new_func)

# Remove the initial updateOrientation call to prevent jumping if video hasn't loaded
old_initial_call = """        hoistedMainListener = mainListener
        controller.addListener(mainListener)
        updateOrientation(controller.videoSize)"""

new_initial_call = """        hoistedMainListener = mainListener
        controller.addListener(mainListener)"""

content = content.replace(old_initial_call, new_initial_call)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)

print("Updated PlayerScreen orientation logic")
