import re

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

old_block = """        // Play icon update
        val player = com.example.service.PlayerManager.exoPlayer
        if (player != null && player.isPlaying) {
            views.setImageViewResource(R.id.widget_btn_play, R.drawable.ic_widget_pause)
        } else {
            views.setImageViewResource(R.id.widget_btn_play, R.drawable.ic_widget_play)
        }"""

new_block = """        // Play icon update
        val player = com.example.service.PlayerManager.exoPlayer
        if (player != null) {
            if (player.isPlaying) {
                views.setImageViewResource(R.id.widget_btn_play, R.drawable.ic_widget_pause)
            } else {
                views.setImageViewResource(R.id.widget_btn_play, R.drawable.ic_widget_play)
            }
            
            // Loop icon
            val loopMode = player.repeatMode
            val primaryColor = android.graphics.Color.parseColor("#3F51B5")
            val defaultColor = android.graphics.Color.parseColor("#19202D")
            
            if (loopMode == androidx.media3.common.Player.REPEAT_MODE_ONE) {
                views.setImageViewResource(R.id.widget_btn_loop, R.drawable.ic_widget_loop_one)
                views.setInt(R.id.widget_btn_loop, "setColorFilter", primaryColor)
            } else if (loopMode == androidx.media3.common.Player.REPEAT_MODE_ALL) {
                views.setImageViewResource(R.id.widget_btn_loop, R.drawable.ic_widget_loop)
                views.setInt(R.id.widget_btn_loop, "setColorFilter", primaryColor)
            } else {
                views.setImageViewResource(R.id.widget_btn_loop, R.drawable.ic_widget_loop)
                views.setInt(R.id.widget_btn_loop, "setColorFilter", defaultColor)
            }
            
            // Shuffle icon
            if (player.shuffleModeEnabled) {
                views.setInt(R.id.widget_btn_shuffle, "setColorFilter", primaryColor)
            } else {
                views.setInt(R.id.widget_btn_shuffle, "setColorFilter", defaultColor)
            }
            
        } else {
            views.setImageViewResource(R.id.widget_btn_play, R.drawable.ic_widget_play)
            views.setInt(R.id.widget_btn_loop, "setColorFilter", android.graphics.Color.parseColor("#19202D"))
            views.setInt(R.id.widget_btn_shuffle, "setColorFilter", android.graphics.Color.parseColor("#19202D"))
        }"""
        
content = content.replace(old_block, new_block)

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
    f.write(content)
print("Added loop and shuffle states")
