with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

target = """                        IconButton(onClick = { 
                            player?.stop()
                            player?.clearMediaItems()
                            onClose() 
                        }) {
                            Icon(Icons.Filled.Close, contentDescription = "Close", tint = androidx.compose.ui.graphics.Color(0xFF2196F3), modifier = Modifier.size(24.dp))
                        }"""

replacement = """                        val context = LocalContext.current
                        val coroutineScope = rememberCoroutineScope()
                        IconButton(onClick = { 
                            player?.stop()
                            player?.clearMediaItems()
                            coroutineScope.launch(kotlinx.coroutines.Dispatchers.IO) {
                                try {
                                    val db = com.example.data.AppDatabase.getDatabase(context)
                                    val repo = com.example.data.PlaylistRepository(db.playlistDao())
                                    val playlists = kotlinx.coroutines.flow.first(repo.getAllPlaylists())
                                    playlists.find { it.name == "Temp Current" }?.let { 
                                        repo.deletePlaylist(it) 
                                    }
                                } catch(e: Exception) {
                                    e.printStackTrace()
                                }
                            }
                            onClose() 
                        }) {
                            Icon(Icons.Filled.Close, contentDescription = "Close", tint = androidx.compose.ui.graphics.Color(0xFF2196F3), modifier = Modifier.size(24.dp))
                        }"""

content = content.replace(target, replacement)
content = content.replace("import kotlinx.coroutines.flow.first\n", "")
content = "import kotlinx.coroutines.flow.first\n" + content

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
