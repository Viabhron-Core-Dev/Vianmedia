with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    content = f.read()

target = """                val views = android.widget.RemoteViews(packageName, com.example.R.layout.widget_media)
                views.setTextViewText(com.example.R.id.widget_title, player.currentMediaItem?.mediaMetadata?.title?.toString() ?: "No Media")
                views.setImageViewResource(com.example.R.id.widget_btn_play, if (player.isPlaying) com.example.R.drawable.ic_widget_pause else com.example.R.drawable.ic_widget_play)"""

replacement = """                val views = android.widget.RemoteViews(packageName, com.example.R.layout.widget_media)
                views.setTextViewText(com.example.R.id.widget_title, player.currentMediaItem?.mediaMetadata?.title?.toString() ?: "No Media")
                views.setImageViewResource(com.example.R.id.widget_btn_play, if (player.isPlaying) com.example.R.drawable.ic_widget_pause else com.example.R.drawable.ic_widget_play)
                val duration = player.duration.coerceAtLeast(1)
                val position = player.currentPosition
                val progress = if (duration > 0) ((position.toFloat() / duration.toFloat()) * 100).toInt() else 0
                views.setProgressBar(com.example.R.id.widget_progress, 100, progress, false)"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/service/PlaybackService.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
