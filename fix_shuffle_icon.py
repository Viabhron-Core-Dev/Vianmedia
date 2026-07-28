with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    content = f.read()

target = "views.setImageViewResource(com.example.R.id.widget_btn_loop, loopIcon)"
replacement = """views.setImageViewResource(com.example.R.id.widget_btn_loop, loopIcon)
                
                // Shuffle icon
                val shuffleIconId = if (player.shuffleModeEnabled) {
                    com.example.R.drawable.ic_widget_shuffle // wait, active color should be primary? Let's just create an active version or use colorFilter.
                } else {
                    com.example.R.drawable.ic_widget_shuffle
                }
                // RemoteViews in API < 31 doesn't support setImageViewColorFilter easily without workarounds. We will create ic_widget_shuffle_active later.
"""
content = content.replace(target, replacement)
with open("app/src/main/java/com/example/service/PlaybackService.kt", "w") as f:
    f.write(content)
