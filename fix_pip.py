import re
with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

pip_block = """        val pipListener = object : androidx.media3.common.Player.Listener {
            override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
                PipHelper.updatePipParams(context, controller, videoSize.width, videoSize.height)
            }
            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_IS_PLAYING_CHANGED) || events.contains(androidx.media3.common.Player.EVENT_MEDIA_ITEM_TRANSITION)) {
                    PipHelper.updatePipParams(context, player, player.videoSize.width, player.videoSize.height)
                }
            }
        }"""

new_pip_block = """        val pipListener = object : androidx.media3.common.Player.Listener {
            override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
                val w = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.width else videoSize.height
                val h = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.height else videoSize.width
                PipHelper.updatePipParams(context, controller, w, h)
            }
            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_IS_PLAYING_CHANGED) || events.contains(androidx.media3.common.Player.EVENT_MEDIA_ITEM_TRANSITION)) {
                    val vs = player.videoSize
                    val w = if (vs.unappliedRotationDegrees % 180 == 0) vs.width else vs.height
                    val h = if (vs.unappliedRotationDegrees % 180 == 0) vs.height else vs.width
                    PipHelper.updatePipParams(context, player, w, h)
                }
            }
        }"""

content = content.replace(pip_block, new_pip_block)

pip_initial = """        PipHelper.updatePipParams(context, controller, controller.videoSize.width, controller.videoSize.height)"""
new_pip_initial = """        val vs = controller.videoSize
        val w = if (vs.unappliedRotationDegrees % 180 == 0) vs.width else vs.height
        val h = if (vs.unappliedRotationDegrees % 180 == 0) vs.height else vs.width
        PipHelper.updatePipParams(context, controller, w, h)"""

content = content.replace(pip_initial, new_pip_initial)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
