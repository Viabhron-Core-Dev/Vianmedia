import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

old_block = """        val savedOrientation = settingsManager.getVideoOrientation(decodedUriString)
        if (savedOrientation != null) {
            context.findActivity()?.requestedOrientation = if (savedOrientation) {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            } else {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            }
        } else {
            context.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
        }

        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
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

new_block = """        val savedOrientation = settingsManager.getVideoOrientation(decodedUriString)
        if (savedOrientation != null) {
            context.findActivity()?.requestedOrientation = if (savedOrientation) {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
            } else {
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            }
        } else {
            context.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
        }"""

content = content.replace(old_block, new_block)

old_event = """            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_VIDEO_SIZE_CHANGED)) {
                    updateOrientation(player.videoSize)
                }
            }"""

new_event = """            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                // Do not auto-rotate based on video size, let native sensors take control
            }"""

content = content.replace(old_event, new_event)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
