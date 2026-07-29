import re

with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    content = f.read()

# Remove loop and shuffle icon updates
content = re.sub(r'val loopIcon = when.*?views\.setImageViewResource\(com\.example\.R\.id\.widget_btn_shuffle, shuffleIconId\)', '', content, flags=re.DOTALL)

# Add progress update to updateWidgetUI
new_update_ui = """            for (appWidgetId in appWidgetIds) {
                val views = android.widget.RemoteViews(packageName, com.example.R.layout.widget_media)
                views.setTextViewText(com.example.R.id.widget_title, player.currentMediaItem?.mediaMetadata?.title?.toString() ?: "No Media")
                views.setImageViewResource(com.example.R.id.widget_btn_play, if (player.isPlaying) com.example.R.drawable.ic_widget_pause else com.example.R.drawable.ic_widget_play)
                
                val duration = player.duration.coerceAtLeast(0)
                val position = player.currentPosition.coerceAtLeast(0)
                views.setProgressBar(com.example.R.id.widget_progress, duration.toInt(), position.toInt(), false)

                appWidgetManager.updateAppWidget(appWidgetId, views)
                appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetId, com.example.R.id.widget_list)
            }"""
content = re.sub(r'for \(appWidgetId in appWidgetIds\) \{.*?appWidgetManager\.notifyAppWidgetViewDataChanged\(appWidgetId, com\.example\.R\.id\.widget_list\)\n\s*\}', new_update_ui, content, flags=re.DOTALL)

# Add handling for ACTION_MINIPLAYER and ACTION_CLOSE
receiver_handling = """            val player = PlayerManager.exoPlayer ?: return
            when (command) {
                "ACTION_MINIPLAYER" -> showOverlay()
                "ACTION_CLOSE" -> {
                    player.stop()
                    player.clearMediaItems()
                    hideOverlay()
                    stopSelf()
                }"""
content = content.replace("            val player = PlayerManager.exoPlayer ?: return\n            when (command) {", receiver_handling)

with open("app/src/main/java/com/example/service/PlaybackService.kt", "w") as f:
    f.write(content)
