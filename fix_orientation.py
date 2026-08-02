import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

# Replace updateOrientation usage in listener
old_listener = """            override fun onPlaybackStateChanged(playbackState: Int) {
                if (playbackState == androidx.media3.common.Player.STATE_READY) {
                    updateOrientation(controller.videoSize)
                }"""
new_listener = """            override fun onPlaybackStateChanged(playbackState: Int) {"""
content = content.replace(old_listener, new_listener)

old_video_size = """            override fun onVideoSizeChanged(videoSize: VideoSize) {
                updateOrientation(videoSize)
            }"""
new_video_size = """            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_VIDEO_SIZE_CHANGED)) {
                    updateOrientation(player.videoSize)
                }
            }"""
content = content.replace(old_video_size, new_video_size)

# Add initial updateOrientation call
old_hoisted = """        hoistedMainListener = mainListener
        controller.addListener(mainListener)"""
new_hoisted = """        hoistedMainListener = mainListener
        controller.addListener(mainListener)
        updateOrientation(controller.videoSize)"""
content = content.replace(old_hoisted, new_hoisted)

# Make sure onDispose uses UNSPECIFIED
old_dispose_user = "context.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_USER"
new_dispose_unspec = "context.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED"
content = content.replace(old_dispose_user, new_dispose_unspec)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)

print("Fixed orientation logic")
