import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

old_block_1 = """            private fun updateOrientation(videoSize: VideoSize) {
                if (videoSize.width > 0 && videoSize.height > 0) {
                    val isRotated = videoSize.unappliedRotationDegrees == 90 || videoSize.unappliedRotationDegrees == 270
                    val effectiveWidth = if (isRotated) videoSize.height else videoSize.width
                    val effectiveHeight = if (isRotated) videoSize.width else videoSize.height
                    context.findActivity()?.requestedOrientation = if (effectiveWidth > effectiveHeight) {
                        ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                    } else {
                        ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                    }
                }
            }"""

new_block_1 = """            private fun updateOrientation(videoSize: VideoSize) {
                if (videoSize.width > 0 && videoSize.height > 0) {
                    context.findActivity()?.requestedOrientation = if (videoSize.height > videoSize.width) {
                        ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                    } else {
                        ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                    }
                }
            }"""

old_block_2 = """        if (currentUri == decodedUriStr && currentVideoSize.width > 0 && currentVideoSize.height > 0) {
            val isRotated = controller.videoSize.unappliedRotationDegrees == 90 || controller.videoSize.unappliedRotationDegrees == 270
            val effectiveWidth = if (isRotated) currentVideoSize.height else currentVideoSize.width
            val effectiveHeight = if (isRotated) currentVideoSize.width else currentVideoSize.height
            context.findActivity()?.requestedOrientation = if (effectiveWidth > effectiveHeight) {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            } else {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            }
        }"""

new_block_2 = """        if (currentUri == decodedUriStr && currentVideoSize.width > 0 && currentVideoSize.height > 0) {
            context.findActivity()?.requestedOrientation = if (currentVideoSize.height > currentVideoSize.width) {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            } else {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            }
        }"""

if old_block_1 in content and old_block_2 in content:
    content = content.replace(old_block_1, new_block_1)
    content = content.replace(old_block_2, new_block_2)
    with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
        f.write(content)
    print("Replaced orientation logic")
else:
    print("Blocks not found!")
