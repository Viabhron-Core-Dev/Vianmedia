with open("app/src/main/java/com/example/service/PlayerManager.kt", "r") as f:
    content = f.read()

target = """        exoPlayer?.addListener(object : androidx.media3.common.Player.Listener {
            override fun onAudioSessionIdChanged(audioSessionId: Int) {"""

replacement = """        exoPlayer?.addListener(object : androidx.media3.common.Player.Listener {
            override fun onPlaybackStateChanged(playbackState: Int) {
                if (playbackState == androidx.media3.common.Player.STATE_ENDED || playbackState == androidx.media3.common.Player.STATE_IDLE) {
                    val count = exoPlayer?.mediaItemCount ?: 0
                    if (playbackState == androidx.media3.common.Player.STATE_ENDED || count == 0) {
                        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
                            try {
                                val db = com.example.data.AppDatabase.getDatabase(context)
                                val repo = com.example.data.PlaylistRepository(db.playlistDao())
                                val temp = repo.getAllPlaylistsSync().find { it.name == "Temp Current" }
                                if (temp != null) {
                                    repo.deletePlaylistById(temp.id)
                                }
                            } catch (e: Exception) {}
                        }
                    }
                }
            }

            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_TIMELINE_CHANGED)) {
                    if (player.mediaItemCount == 0) {
                        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
                            try {
                                val db = com.example.data.AppDatabase.getDatabase(context)
                                val repo = com.example.data.PlaylistRepository(db.playlistDao())
                                val temp = repo.getAllPlaylistsSync().find { it.name == "Temp Current" }
                                if (temp != null) {
                                    repo.deletePlaylistById(temp.id)
                                }
                            } catch (e: Exception) {}
                        }
                    }
                }
            }
            override fun onAudioSessionIdChanged(audioSessionId: Int) {"""

content = content.replace(target, replacement)
content = "import kotlinx.coroutines.launch\n" + content

with open("app/src/main/java/com/example/service/PlayerManager.kt", "w") as f:
    f.write(content)
