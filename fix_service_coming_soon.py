import re

with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "r") as f:
    content = f.read()

count_block = """    override fun getCount(): Int {
        return when (currentMode) {
            "root" -> 3
            "current" -> playlist.size
            "folders" -> folders.size
            "folder_items", "search_results" -> folderItems.size
            "playlists" -> 0 // Placeholder
            else -> 0
        }
    }"""

new_count_block = """    override fun getCount(): Int {
        return when (currentMode) {
            "root" -> 3
            "current" -> playlist.size
            "folders", "playlists" -> 1
            "folder_items", "search_results" -> folderItems.size
            else -> 0
        }
    }"""

content = content.replace(count_block, new_count_block)

view_block = """                "folders" -> {
                    views.setViewVisibility(R.id.widget_item_icon, android.view.View.GONE)
                    val folder = folders[position]
                    views.setTextViewText(R.id.widget_item_title, folder.name)
                    views.setOnClickFillInIntent(R.id.widget_item_root, Intent().putExtra("FOLDER_ID", folder.id).putExtra("WIDGET_ACTION", "OPEN_FOLDER"))
                }"""

new_view_block = """                "folders", "playlists" -> {
                    views.setViewVisibility(R.id.widget_item_icon, android.view.View.GONE)
                    views.setTextViewText(R.id.widget_item_title, "Feature coming soon")
                    views.setInt(R.id.widget_item_root, "setBackgroundColor", android.graphics.Color.TRANSPARENT)
                    views.setOnClickFillInIntent(R.id.widget_item_root, Intent())
                }"""

content = content.replace(view_block, new_view_block)

with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "w") as f:
    f.write(content)
print("Updated MediaWidgetService with coming soon")
