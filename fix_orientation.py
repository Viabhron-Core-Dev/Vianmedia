import re
with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

old_func = """            private fun updateOrientation(videoSize: VideoSize) {
                if (videoSize.width > 0 && videoSize.height > 0) {
                    context.findActivity()?.requestedOrientation = if (videoSize.height > videoSize.width) {
                        ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                    } else {
                        ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                    }
                }
            }"""

new_func = """            private fun updateOrientation(videoSize: VideoSize) {
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

content = content.replace(old_func, new_func)

old_initial = """        val currentVideoSize = controller.videoSize
        val currentUri = controller.currentMediaItem?.localConfiguration?.uri?.toString()
        if (currentUri == decodedUriString && currentVideoSize.width > 0 && currentVideoSize.height > 0) {
            context.findActivity()?.requestedOrientation = if (currentVideoSize.height > currentVideoSize.width) {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            } else {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            }
        }"""

new_initial = """        val currentVideoSize = controller.videoSize
        val currentUri = controller.currentMediaItem?.localConfiguration?.uri?.toString()
        if (currentUri == decodedUriString && currentVideoSize.width > 0 && currentVideoSize.height > 0) {
            val isPortrait = if (currentVideoSize.unappliedRotationDegrees % 180 == 0) {
                currentVideoSize.height > currentVideoSize.width
            } else {
                currentVideoSize.width > currentVideoSize.height
            }
            context.findActivity()?.requestedOrientation = if (isPortrait) {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            } else {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            }
        }"""

content = content.replace(old_initial, new_initial)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
print("Applied orientation logic fix.")
