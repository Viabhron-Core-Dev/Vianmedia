import re
with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

# Remove initial orientation block
initial_block = """        val currentVideoSize = controller.videoSize
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

if initial_block in content:
    content = content.replace(initial_block, "")
    print("Removed initial block")

# Remove updateOrientation in EVENT_MEDIA_ITEM_TRANSITION
events_block = """            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_MEDIA_ITEM_TRANSITION)) {
                    updateOrientation(player.videoSize)
                }
            }"""

if events_block in content:
    content = content.replace(events_block, "")
    print("Removed onEvents block")

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
