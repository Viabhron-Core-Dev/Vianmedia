with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

target = """                if (found && playlistItems.size > 1) {
                    kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                        if (controller.currentMediaItem?.mediaId == decodedUri.toString()) {
                            val currentPos = controller.currentPosition
                            val isPlaying = controller.isPlaying
                            controller.setMediaItems(playlistItems, startIndex, currentPos)
                            if (isPlaying) {
                                controller.play()
                            }
                        }
                    }
                }"""

replacement = """                if (found && playlistItems.size > 1) {
                    kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                        if (controller.currentMediaItem?.mediaId == decodedUri.toString()) {
                            val currentPos = controller.currentPosition
                            val isPlaying = controller.isPlaying
                            controller.setMediaItems(playlistItems, startIndex, currentPos)
                            if (isPlaying) {
                                controller.play()
                            }
                        }
                    }
                    
                    // Generate Temp Current playlist
                    try {
                        val db = com.example.data.AppDatabase.getDatabase(context)
                        val playlistRepo = com.example.data.PlaylistRepository(db.playlistDao())
                        val existingTemp = kotlinx.coroutines.flow.first(playlistRepo.getAllPlaylists()).find { it.name == "Temp Current" }
                        val tempPlaylistId = if (existingTemp != null) {
                            existingTemp.id
                        } else {
                            val newPlaylist = com.example.data.Playlist(name = "Temp Current")
                            playlistRepo.insertPlaylist(newPlaylist).toInt()
                        }
                        
                        // clear existing items
                        val existingItems = kotlinx.coroutines.flow.first(playlistRepo.getItemsForPlaylist(tempPlaylistId))
                        existingItems.forEach { playlistRepo.deletePlaylistItem(it) }
                        
                        // insert new items
                        val time = System.currentTimeMillis()
                        playlistItems.forEachIndexed { i, item ->
                            val pItem = com.example.data.PlaylistItem(
                                playlistId = tempPlaylistId,
                                mediaUri = item.mediaId,
                                displayName = item.mediaMetadata.title.toString(),
                                timestamp = time - i * 1000 // descending order
                            )
                            playlistRepo.insertPlaylistItem(pItem)
                        }
                    } catch(e: Exception) {
                        e.printStackTrace()
                    }
                }"""

content = content.replace(target, replacement)
content = content.replace("import kotlinx.coroutines.flow.first\n", "")
content = "import kotlinx.coroutines.flow.first\n" + content

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
