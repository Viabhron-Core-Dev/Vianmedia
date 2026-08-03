with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

old_code = """        context.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
        val mainListener = object : androidx.media3.common.Player.Listener {"""

new_code = """        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
            if (videoSize.width > 0 && videoSize.height > 0) {
                val isPortrait = videoSize.height > videoSize.width
                context.findActivity()?.requestedOrientation = if (isPortrait) {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                } else {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                }
            }
        }

        updateOrientation(controller.videoSize)
        val mainListener = object : androidx.media3.common.Player.Listener {"""

content = content.replace(old_code, new_code)

old_events = """            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                // Do not auto-rotate based on video size, let native sensors take control
            }"""

new_events = """            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_VIDEO_SIZE_CHANGED)) {
                    updateOrientation(player.videoSize)
                }
            }"""

content = content.replace(old_events, new_events)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
