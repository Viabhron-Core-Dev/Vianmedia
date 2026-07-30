import re

with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "r") as f:
    content = f.read()

target = """    override fun onDataSetChanged() {
        com.example.LogKeeper.log("onDataSetChanged started", "MediaWidgetFactory")
        try {
        val player = PlayerManager.exoPlayer
        
        if (player == null || player.currentTimeline.isEmpty || !player.isPlaying) {
            mode = "FOLDERS"
        } else {
            mode = "PLAYLIST"
        }
        
        val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
        folderId = prefs.getString("folder_id", null)
        
        if (mode == "PLAYLIST") {
            val items = mutableListOf<MediaItem>()
            for (i in 0 until player!!.currentTimeline.windowCount) {
                val window = androidx.media3.common.Timeline.Window()
                player.currentTimeline.getWindow(i, window)
                items.add(window.mediaItem)
            }
            playlist = items
        } else if (mode == "FOLDERS") {
            runBlocking {
                val repo = MediaRepository(context)
                val allFolders = repo.getMediaFolders()
                folders = allFolders
                
                if (folderId != null) {
                    folderItems = folders.find { it.id == folderId }?.mediaItems ?: emptyList()
                } else {
                    folderItems = emptyList()
                }
            }
        }
        com.example.LogKeeper.log("onDataSetChanged finished successfully. Mode: $mode", "MediaWidgetFactory")
        } catch (e: Exception) {
            com.example.LogKeeper.logError("MediaWidgetFactory", "Error in onDataSetChanged", e)
        }
    }"""

replacement = """    override fun onDataSetChanged() {
        com.example.LogKeeper.log("onDataSetChanged started", "MediaWidgetFactory")
        try {
            var isPlayerActive = false
            val items = mutableListOf<MediaItem>()
            
            // ExoPlayer must be accessed on its application thread (main thread)
            runBlocking {
                kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                    val player = PlayerManager.exoPlayer
                    if (player != null && !player.currentTimeline.isEmpty && player.isPlaying) {
                        isPlayerActive = true
                        for (i in 0 until player.currentTimeline.windowCount) {
                            val window = androidx.media3.common.Timeline.Window()
                            player.currentTimeline.getWindow(i, window)
                            items.add(window.mediaItem)
                        }
                    }
                }
            }

            if (isPlayerActive) {
                mode = "PLAYLIST"
                playlist = items
            } else {
                mode = "FOLDERS"
            }
            
            val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
            folderId = prefs.getString("folder_id", null)
            
            if (mode == "FOLDERS") {
                runBlocking {
                    val repo = MediaRepository(context)
                    val allFolders = repo.getMediaFolders()
                    folders = allFolders
                    
                    if (folderId != null) {
                        folderItems = folders.find { it.id == folderId }?.mediaItems ?: emptyList()
                    } else {
                        folderItems = emptyList()
                    }
                }
            }
            com.example.LogKeeper.log("onDataSetChanged finished successfully. Mode: $mode", "MediaWidgetFactory")
        } catch (e: Exception) {
            com.example.LogKeeper.logError("MediaWidgetFactory", "Error in onDataSetChanged", e)
        }
    }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
