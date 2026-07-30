import re

with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "r") as f:
    content = f.read()

# Update getCount
count_old = """    override fun getCount(): Int {
        try {
        if (mode == "PLAYLIST") return playlist.size
        if (mode == "FOLDERS") {
            if (folderId == null) return folders.size
            else return folderItems.size + 1 // +1 for "Up" button
        }
        return 0
        } catch (e: Exception) {
            com.example.LogKeeper.logError("MediaWidgetFactory", "Error in getCount", e)
            return 0
        }
    }"""
count_new = """    override fun getCount(): Int {
        try {
        if (mode == "PLAYLIST") return playlist.size
        if (mode == "FOLDERS") {
            if (folderId == null) return folders.size
            else return folderItems.size
        }
        return 0
        } catch (e: Exception) {
            com.example.LogKeeper.logError("MediaWidgetFactory", "Error in getCount", e)
            return 0
        }
    }"""
content = content.replace(count_old, count_new)

# Update getViewAt
view_old = """            } else {
                if (position == 0) {
                    if (folderId == "search_results") {
                        views.setTextViewText(R.id.widget_item_title, "[Clear Search]")
                    } else {
                        views.setTextViewText(R.id.widget_item_title, "[Back to Folders]")
                    }
                    val fillInIntent = Intent().putExtra("WIDGET_ACTION", "BACK_FOLDER")
                    views.setOnClickFillInIntent(R.id.widget_item_root, fillInIntent)
                } else {
                    val file = folderItems[position - 1]
                    views.setTextViewText(R.id.widget_item_title, "[Media] " + file.name)
                    val fillInIntent = Intent()
                        .putExtra("MEDIA_URI", file.uri.toString())
                        .putExtra("WIDGET_ACTION", "PLAY_FILE")
                    views.setOnClickFillInIntent(R.id.widget_item_root, fillInIntent)
                }
            }"""
view_new = """            } else {
                val file = folderItems[position]
                views.setTextViewText(R.id.widget_item_title, "[Media] " + file.name)
                val fillInIntent = Intent()
                    .putExtra("MEDIA_URI", file.uri.toString())
                    .putExtra("WIDGET_ACTION", "PLAY_FILE")
                views.setOnClickFillInIntent(R.id.widget_item_root, fillInIntent)
            }"""
content = content.replace(view_old, view_new)

with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "w") as f:
    f.write(content)
print("Updated MediaWidgetService")
