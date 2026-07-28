with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    content = f.read()

target1 = "views.setImageViewResource(com.example.R.id.widget_btn_play, if (player.isPlaying) android.R.drawable.ic_media_pause else android.R.drawable.ic_media_play)"
replacement1 = "views.setImageViewResource(com.example.R.id.widget_btn_play, if (player.isPlaying) com.example.R.drawable.ic_widget_pause else com.example.R.drawable.ic_widget_play)"
content = content.replace(target1, replacement1)

target2 = "else -> com.example.R.drawable.ic_loop_all_inactive"
replacement2 = "else -> com.example.R.drawable.ic_widget_loop"
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/PlaybackService.kt", "w") as f:
    f.write(content)
