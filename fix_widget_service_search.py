with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "r") as f:
    content = f.read()

target = """            if (mode == "FOLDERS") {
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

replacement = """            if (mode == "FOLDERS") {
                runBlocking {
                    val repo = MediaRepository(context)
                    val allFolders = repo.getMediaFolders()
                    val searchQuery = prefs.getString("search_query", "") ?: ""
                    
                    if (searchQuery.isNotBlank()) {
                        val allItems = allFolders.flatMap { it.mediaItems }
                        val filteredItems = allItems.filter { it.name.contains(searchQuery, ignoreCase = true) }
                        folders = emptyList()
                        folderId = "search_results" // Virtual folder
                        folderItems = filteredItems
                    } else {
                        folders = allFolders
                        if (folderId != null && folderId != "search_results") {
                            folderItems = folders.find { it.id == folderId }?.mediaItems ?: emptyList()
                        } else {
                            folderItems = emptyList()
                            folderId = null
                        }
                    }
                }
            }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
