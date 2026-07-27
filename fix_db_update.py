with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "r") as f:
    content = f.read()

target = """                                                            val newTimestamps = playlistItems.map { it.timestamp }
                                                            coroutineScope.launch {
                                                                localPlaylistItems.forEachIndexed { i, localItem ->
                                                                    if (localItem.timestamp != newTimestamps[i]) {
                                                                        repository.updatePlaylistItem(localItem.copy(timestamp = newTimestamps[i]))
                                                                    }
                                                                }
                                                            }"""

replacement = """                                                            val newTimestamps = playlistItems.map { it.timestamp }
                                                            val itemsToUpdate = mutableListOf<com.example.data.PlaylistItem>()
                                                            localPlaylistItems.forEachIndexed { i, localItem ->
                                                                if (localItem.timestamp != newTimestamps[i]) {
                                                                    itemsToUpdate.add(localItem.copy(timestamp = newTimestamps[i]))
                                                                }
                                                            }
                                                            if (itemsToUpdate.isNotEmpty()) {
                                                                coroutineScope.launch {
                                                                    repository.updatePlaylistItems(itemsToUpdate)
                                                                }
                                                            }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "w") as f:
    f.write(content)
