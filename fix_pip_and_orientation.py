import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

# Fix updateOrientation
old_update = """        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
            if (videoSize.width > 0 && videoSize.height > 0) {
                val isPortrait = videoSize.height > videoSize.width
                context.findActivity()?.requestedOrientation = if (isPortrait) {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                } else {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                }
            }
        }"""

new_update = """        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
            if (videoSize.width > 0 && videoSize.height > 0) {
                @Suppress("DEPRECATION")
                val w = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.width else videoSize.height
                @Suppress("DEPRECATION")
                val h = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.height else videoSize.width
                val isPortrait = h > w
                context.findActivity()?.requestedOrientation = if (isPortrait) {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                } else {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                }
            }
        }"""

content = content.replace(old_update, new_update)

# Make sure updateOrientation is called on MEDIA_ITEM_TRANSITION
old_events = """            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_VIDEO_SIZE_CHANGED)) {
                    updateOrientation(player.videoSize)
                }
            }"""

new_events = """            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_VIDEO_SIZE_CHANGED) || events.contains(androidx.media3.common.Player.EVENT_MEDIA_ITEM_TRANSITION)) {
                    updateOrientation(player.videoSize)
                }
            }"""

content = content.replace(old_events, new_events)

# Fix PiP permission check
old_pip_check = """                                    if (mode != android.app.AppOpsManager.MODE_ALLOWED) {"""
new_pip_check = """                                    if (mode != android.app.AppOpsManager.MODE_ALLOWED && mode != android.app.AppOpsManager.MODE_DEFAULT) {"""
content = content.replace(old_pip_check, new_pip_check)

# Fix PipHelper call width and height to account for rotation
old_pip_call = """                                                val width = mediaController?.videoSize?.width ?: 0
                                                val height = mediaController?.videoSize?.height ?: 0
                                                val params = PipHelper.buildPipParams(context, mediaController, width, height)"""

new_pip_call = """                                                val vs = mediaController?.videoSize
                                                val rot = vs?.unappliedRotationDegrees ?: 0
                                                val width = if (rot % 180 == 0) vs?.width ?: 0 else vs?.height ?: 0
                                                val height = if (rot % 180 == 0) vs?.height ?: 0 else vs?.width ?: 0
                                                val params = PipHelper.buildPipParams(context, mediaController, width, height)"""

content = content.replace(old_pip_call, new_pip_call)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    overlay_content = f.read()

old_overlay_check = """                        if (mode == android.app.AppOpsManager.MODE_ALLOWED) {"""
new_overlay_check = """                        if (mode == android.app.AppOpsManager.MODE_ALLOWED || mode == android.app.AppOpsManager.MODE_DEFAULT) {"""
overlay_content = overlay_content.replace(old_overlay_check, new_overlay_check)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(overlay_content)
