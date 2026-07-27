with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

target = """                        // clear existing items
                        val existingItems = playlistRepo.getItemsForPlaylist(tempPlaylistId).first()
                        existingItems.forEach { playlistRepo.deletePlaylistItemById(it.id) }
                        
                        // insert new items
                        val time = System.currentTimeMillis()
                        playlistItems.forEachIndexed { i, item ->
                            val pItem = com.example.data.PlaylistItem(
                                playlistId = tempPlaylistId,
                                mediaUri = item.mediaId,
                                timestamp = time - i * 1000 // descending order
                            )
                            playlistRepo.insertPlaylistItem(pItem)
                        }"""

replacement = """                        // clear existing items
                        val existingItems = playlistRepo.getItemsForPlaylist(tempPlaylistId).first()
                        for (item in existingItems) {
                            playlistRepo.deletePlaylistItemById(item.id)
                        }
                        
                        // insert new items
                        val time = System.currentTimeMillis()
                        for (i in playlistItems.indices) {
                            val item = playlistItems[i]
                            val pItem = com.example.data.PlaylistItem(
                                playlistId = tempPlaylistId,
                                mediaUri = item.mediaId,
                                timestamp = time - i * 1000L // descending order
                            )
                            playlistRepo.insertPlaylistItem(pItem)
                        }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
