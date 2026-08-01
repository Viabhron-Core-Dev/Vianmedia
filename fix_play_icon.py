import re

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

old_block = """        // Hierarchy UI Update
        val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)"""

new_block = """        // Play icon update
        val player = com.example.service.PlayerManager.exoPlayer
        if (player != null && player.isPlaying) {
            views.setImageViewResource(R.id.widget_btn_play, R.drawable.ic_widget_pause)
        } else {
            views.setImageViewResource(R.id.widget_btn_play, R.drawable.ic_widget_play)
        }

        // Hierarchy UI Update
        val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)"""
        
if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
        f.write(content)
    print("Fixed play icon")
else:
    print("Could not find block")
