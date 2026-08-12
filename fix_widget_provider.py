import sys

with open('app/src/main/java/com/example/widget/MediaWidgetProvider.kt', 'r') as f:
    content = f.read()

target1 = """            if (searchQuery?.isNotBlank() == true) {
                prefs.edit().putString("search_query", "").apply()
            } else if (currentMode == "folder_items") {
                prefs.edit().putString("explorer_mode", "folders").putString("folder_id", null).apply()
            } else if (currentMode == "folders" || currentMode == "current" || currentMode == "playlists") {
                prefs.edit().putString("explorer_mode", "root").apply()
            }"""

replacement1 = """            if (searchQuery?.isNotBlank() == true) {
                prefs.edit().putString("search_query", "").apply()
            } else if (currentMode == "folder_items") {
                prefs.edit().putString("explorer_mode", "folders").putString("folder_id", null).apply()
            } else if (currentMode == "playlist_items") {
                prefs.edit().putString("explorer_mode", "playlists").putString("folder_id", null).apply()
            } else if (currentMode == "folders" || currentMode == "current" || currentMode == "playlists") {
                prefs.edit().putString("explorer_mode", "root").apply()
            }"""

if target1 in content:
    content = content.replace(target1, replacement1)
    print("Success 1")

target2 = """                "OPEN_FOLDER" -> {
                    val folderId = intent.getStringExtra("FOLDER_ID")
                    prefs.edit().putString("explorer_mode", "folder_items").putString("folder_id", folderId).apply()
                    updateWidgets(context)
                    return
                }"""

replacement2 = """                "OPEN_FOLDER" -> {
                    val folderId = intent.getStringExtra("EXTRA_FOLDER_ID")
                    prefs.edit().putString("explorer_mode", "folder_items").putString("folder_id", folderId).apply()
                    updateWidgets(context)
                    return
                }
                "OPEN_PLAYLIST" -> {
                    val folderId = intent.getStringExtra("EXTRA_FOLDER_ID")
                    prefs.edit().putString("explorer_mode", "playlist_items").putString("folder_id", folderId).apply()
                    updateWidgets(context)
                    return
                }"""

if target2 in content:
    content = content.replace(target2, replacement2)
    print("Success 2")

with open('app/src/main/java/com/example/widget/MediaWidgetProvider.kt', 'w') as f:
    f.write(content)
