import re

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

# Replace UI Hierarchy logic in updateAppWidget
old_hierarchy = """        // Hierarchy UI Update
        var isPlayerActive = false
        val player = com.example.service.PlayerManager.exoPlayer
        if (player != null && !player.currentTimeline.isEmpty) {
            isPlayerActive = true
        }
        val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
        val folderId = prefs.getString("folder_id", null)
        
        if (isPlayerActive) {
            views.setTextViewText(R.id.widget_explorer_title, "Now Playing")
            views.setViewVisibility(R.id.widget_btn_back, android.view.View.GONE)
        } else {
            if (folderId != null) {
                if (folderId == "search_results") {
                    views.setTextViewText(R.id.widget_explorer_title, "Search Results")
                } else {
                    views.setTextViewText(R.id.widget_explorer_title, "Folder")
                }
                views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
            } else {
                views.setTextViewText(R.id.widget_explorer_title, "Folders")
                views.setViewVisibility(R.id.widget_btn_back, android.view.View.GONE)
            }
        }"""

new_hierarchy = """        // Hierarchy UI Update
        val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
        val currentMode = prefs.getString("explorer_mode", "current") ?: "current"
        val folderId = prefs.getString("folder_id", null)
        val searchQuery = prefs.getString("search_query", "")
        
        if (searchQuery?.isNotBlank() == true) {
            views.setTextViewText(R.id.widget_explorer_title, "Search Results")
            views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
        } else {
            when (currentMode) {
                "root" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Library")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.GONE)
                }
                "current" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Current")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
                "folders" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Folder List")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
                "folder_items" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Folder")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
                "playlists" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Playlists")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
            }
        }"""
content = content.replace(old_hierarchy, new_hierarchy)

# Find onReceive logic for navigation
# We need to inject the navigation action handling
nav_handling = """        if (action == "ACTION_BACK_FOLDER") {
            val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
            val currentMode = prefs.getString("explorer_mode", "current") ?: "current"
            val folderId = prefs.getString("folder_id", null)
            val searchQuery = prefs.getString("search_query", "")
            
            if (searchQuery.isNotBlank()) {
                prefs.edit().putString("search_query", "").apply()
            } else if (currentMode == "folder_items") {
                prefs.edit().putString("explorer_mode", "folders").putString("folder_id", null).apply()
            } else if (currentMode == "folders" || currentMode == "current" || currentMode == "playlists") {
                prefs.edit().putString("explorer_mode", "root").apply()
            }
            
            updateWidgets(context)
            return
        }
"""
# Replace the existing ACTION_BACK_FOLDER if it exists, or insert it.
# First, remove old one if exists:
old_back = """        if (action == "ACTION_BACK_FOLDER") {
            val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
            prefs.edit().putString("folder_id", null).putString("search_query", "").apply()
            
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
            val appWidgetIds = appWidgetManager.getAppWidgetIds(componentName)
            for (id in appWidgetIds) {
                updateAppWidget(context, appWidgetManager, id)
            }
            appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetIds, R.id.widget_list)
            return
        }"""
if old_back in content:
    content = content.replace(old_back, nav_handling)
else:
    # insert before ACTION_PLAY_ITEM
    content = content.replace('if (action == "ACTION_PLAY_ITEM") {', nav_handling + '        if (action == "ACTION_PLAY_ITEM") {')


# Update PLAY_ITEM handling to handle NAVIGATE_*
old_play_item = """        if (action == "ACTION_PLAY_ITEM") {
            val widgetAction = intent.getStringExtra("WIDGET_ACTION")
            if (widgetAction == "PLAY_FILE") {
                val uriStr = intent.getStringExtra("MEDIA_URI")
                if (uriStr != null) {
                    val playIntent = Intent(context, com.example.service.PlaybackService::class.java).apply {
                        this.action = "ACTION_PLAY_URI"
                        putExtra("URI", uriStr)
                    }
                    context.startService(playIntent)
                }
            } else if (widgetAction == "OPEN_FOLDER") {
                val folderId = intent.getStringExtra("FOLDER_ID")
                val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
                prefs.edit().putString("folder_id", folderId).apply()
                
                val appWidgetManager = AppWidgetManager.getInstance(context)
                val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
                val appWidgetIds = appWidgetManager.getAppWidgetIds(componentName)
                for (id in appWidgetIds) {
                    updateAppWidget(context, appWidgetManager, id)
                }
                appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetIds, R.id.widget_list)
            } else if (widgetAction == "PLAYLIST_ITEM") {
                val index = intent.getIntExtra("EXTRA_INDEX", 0)
                val player = com.example.service.PlayerManager.exoPlayer
                player?.seekToDefaultPosition(index)
            }
            return
        }"""
        
new_play_item = """        if (action == "ACTION_PLAY_ITEM") {
            val widgetAction = intent.getStringExtra("WIDGET_ACTION")
            val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
            
            when (widgetAction) {
                "NAVIGATE_CURRENT" -> {
                    prefs.edit().putString("explorer_mode", "current").apply()
                    updateWidgets(context)
                }
                "NAVIGATE_FOLDERS" -> {
                    prefs.edit().putString("explorer_mode", "folders").putString("folder_id", null).apply()
                    updateWidgets(context)
                }
                "NAVIGATE_PLAYLISTS" -> {
                    prefs.edit().putString("explorer_mode", "playlists").apply()
                    updateWidgets(context)
                }
                "PLAY_FILE" -> {
                    val uriStr = intent.getStringExtra("MEDIA_URI")
                    if (uriStr != null) {
                        val playIntent = Intent(context, com.example.service.PlaybackService::class.java).apply {
                            this.action = "ACTION_PLAY_URI"
                            putExtra("URI", uriStr)
                        }
                        context.startService(playIntent)
                    }
                }
                "OPEN_FOLDER" -> {
                    val folderId = intent.getStringExtra("FOLDER_ID")
                    prefs.edit().putString("explorer_mode", "folder_items").putString("folder_id", folderId).apply()
                    updateWidgets(context)
                }
                "PLAYLIST_ITEM" -> {
                    val index = intent.getIntExtra("EXTRA_INDEX", 0)
                    val player = com.example.service.PlayerManager.exoPlayer
                    player?.seekToDefaultPosition(index)
                }
            }
            return
        }"""
if old_play_item in content:
    content = content.replace(old_play_item, new_play_item)
else:
    print("WARNING: Could not replace ACTION_PLAY_ITEM logic")

# add updateWidgets helper
if "private fun updateWidgets(" not in content:
    helper = """
    private fun updateWidgets(context: Context) {
        val appWidgetManager = AppWidgetManager.getInstance(context)
        val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
        val appWidgetIds = appWidgetManager.getAppWidgetIds(componentName)
        for (id in appWidgetIds) {
            updateAppWidget(context, appWidgetManager, id)
        }
        appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetIds, R.id.widget_list)
    }
"""
    content = content.replace("class MediaWidgetProvider : AppWidgetProvider() {", "class MediaWidgetProvider : AppWidgetProvider() {" + helper)
    
with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
    f.write(content)

print("Updated MediaWidgetProvider")
