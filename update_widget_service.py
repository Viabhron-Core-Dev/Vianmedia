import re

with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "r") as f:
    content = f.read()

new_logic = """        val player = PlayerManager.exoPlayer
        
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
        }"""

content = re.sub(r'        val prefs = context.getSharedPreferences\("widget_prefs", Context\.MODE_PRIVATE\).*?        } else if \(mode == "FOLDERS"\) \{.*?            \}\n        \}', new_logic, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "w") as f:
    f.write(content)
