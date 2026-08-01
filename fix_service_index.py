import re

with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "r") as f:
    content = f.read()

# Add currentIndex
content = content.replace("private var playlist = listOf<MediaItem>()", "private var playlist = listOf<MediaItem>()\n    private var currentIndex = -1")

# Fetch currentIndex
old_fetch = """                    val player = PlayerManager.exoPlayer
                    if (player != null && !player.currentTimeline.isEmpty) {
                        for (i in 0 until player.currentTimeline.windowCount) {"""

new_fetch = """                    val player = PlayerManager.exoPlayer
                    if (player != null && !player.currentTimeline.isEmpty) {
                        currentIndex = player.currentMediaItemIndex
                        for (i in 0 until player.currentTimeline.windowCount) {"""
content = content.replace(old_fetch, new_fetch)

# Use currentIndex in getViewAt
old_view = """                "current" -> {
                    views.setViewVisibility(R.id.widget_item_icon, android.view.View.GONE)
                    val item = playlist[position]
                    views.setTextViewText(R.id.widget_item_title, item.mediaMetadata.title?.toString() ?: item.mediaId)
                    views.setOnClickFillInIntent(R.id.widget_item_root, Intent().putExtra("EXTRA_INDEX", position).putExtra("WIDGET_ACTION", "PLAYLIST_ITEM"))
                }"""

new_view = """                "current" -> {
                    views.setViewVisibility(R.id.widget_item_icon, android.view.View.GONE)
                    val item = playlist[position]
                    views.setTextViewText(R.id.widget_item_title, item.mediaMetadata.title?.toString() ?: item.mediaId)
                    
                    if (position == currentIndex) {
                        views.setInt(R.id.widget_item_root, "setBackgroundColor", android.graphics.Color.parseColor("#333F51B5"))
                    } else {
                        views.setInt(R.id.widget_item_root, "setBackgroundColor", android.graphics.Color.TRANSPARENT)
                    }
                    
                    views.setOnClickFillInIntent(R.id.widget_item_root, Intent().putExtra("EXTRA_INDEX", position).putExtra("WIDGET_ACTION", "PLAYLIST_ITEM"))
                }"""
content = content.replace(old_view, new_view)

with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "w") as f:
    f.write(content)
print("Updated MediaWidgetService")
