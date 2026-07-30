import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

pattern1 = r"""            override fun onVideoSizeChanged\(videoSize: VideoSize\) \{
                if \(videoSize\.width > 0 && videoSize\.height > 0\) \{
                    val isRotated = videoSize\.unappliedRotationDegrees == 90 \|\| videoSize\.unappliedRotationDegrees == 270
                    val effectiveWidth = if \(isRotated\) videoSize\.height else videoSize\.width
                    val effectiveHeight = if \(isRotated\) videoSize\.width else videoSize\.height
                    context\.findActivity\(\)\?\.requestedOrientation = if \(effectiveWidth > effectiveHeight\) \{
                        ActivityInfo\.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                    \} else \{
                        ActivityInfo\.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                    \}
                \}
            \}"""

replacement1 = """            override fun onVideoSizeChanged(videoSize: VideoSize) {
                if (videoSize.width > 0 && videoSize.height > 0) {
                    context.findActivity()?.requestedOrientation = if (videoSize.width > videoSize.height) {
                        ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                    } else {
                        ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                    }
                }
            }"""

content = re.sub(pattern1, replacement1, content)

pattern2 = r"""        val currentVideoSize = controller\.videoSize
        if \(currentVideoSize\.width > 0 && currentVideoSize\.height > 0\) \{
            val isRotated = currentVideoSize\.unappliedRotationDegrees == 90 \|\| currentVideoSize\.unappliedRotationDegrees == 270
            val effectiveWidth = if \(isRotated\) currentVideoSize\.height else currentVideoSize\.width
            val effectiveHeight = if \(isRotated\) currentVideoSize\.width else currentVideoSize\.height
            context\.findActivity\(\)\?\.requestedOrientation = if \(effectiveWidth > effectiveHeight\) \{
                ActivityInfo\.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            \} else \{
                ActivityInfo\.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            \}
        \}"""

replacement2 = """        val currentVideoSize = controller.videoSize
        if (currentVideoSize.width > 0 && currentVideoSize.height > 0) {
            context.findActivity()?.requestedOrientation = if (currentVideoSize.width > currentVideoSize.height) {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            } else {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            }
        }"""

content = re.sub(pattern2, replacement2, content)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
print("reverted")
