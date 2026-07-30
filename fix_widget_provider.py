import re

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

# 1. Update updateAppWidget intents and dynamic states
intents_old = """        // Intents for playback controls
        views.setOnClickPendingIntent(R.id.widget_btn_prev, getPendingIntent(context, "ACTION_PREV"))
        views.setOnClickPendingIntent(R.id.widget_btn_play, getPendingIntent(context, "ACTION_PLAY_PAUSE"))
        views.setOnClickPendingIntent(R.id.widget_btn_next, getPendingIntent(context, "ACTION_NEXT"))
        views.setOnClickPendingIntent(R.id.widget_btn_loop, getPendingIntent(context, "ACTION_LOOP"))
        views.setOnClickPendingIntent(R.id.widget_btn_shuffle, getPendingIntent(context, "ACTION_SHUFFLE"))
        
        // Bottom right intents
        views.setOnClickPendingIntent(R.id.widget_btn_close, getPendingIntent(context, "ACTION_CLOSE"))
        views.setOnClickPendingIntent(R.id.widget_btn_miniplayer, getPendingIntent(context, "ACTION_MINIPLAYER"))"""

intents_new = """        // Intents for playback controls
        views.setOnClickPendingIntent(R.id.widget_btn_prev, getPendingIntent(context, "ACTION_PREV"))
        views.setOnClickPendingIntent(R.id.widget_btn_rewind, getPendingIntent(context, "ACTION_REWIND"))
        views.setOnClickPendingIntent(R.id.widget_btn_play, getPendingIntent(context, "ACTION_PLAY_PAUSE"))
        views.setOnClickPendingIntent(R.id.widget_btn_ffwd, getPendingIntent(context, "ACTION_FFWD"))
        views.setOnClickPendingIntent(R.id.widget_btn_next, getPendingIntent(context, "ACTION_NEXT"))
        views.setOnClickPendingIntent(R.id.widget_btn_stop, getPendingIntent(context, "ACTION_STOP"))
        views.setOnClickPendingIntent(R.id.widget_btn_loop, getPendingIntent(context, "ACTION_LOOP"))
        views.setOnClickPendingIntent(R.id.widget_btn_shuffle, getPendingIntent(context, "ACTION_SHUFFLE"))
        
        // Bottom right intents
        views.setOnClickPendingIntent(R.id.widget_btn_close, getPendingIntent(context, "ACTION_CLOSE"))
        views.setOnClickPendingIntent(R.id.widget_btn_miniplayer, getPendingIntent(context, "ACTION_MINIPLAYER"))
        
        views.setOnClickPendingIntent(R.id.widget_btn_back, getPendingIntent(context, "ACTION_BACK_FOLDER"))
        
        // Hierarchy UI Update
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
content = content.replace(intents_old, intents_new)

# 2. Update onReceive for new actions
receive_old = """        if (action == "ACTION_OPEN_APP") {"""
receive_new = """        if (action == "ACTION_REWIND") {
            val player = com.example.service.PlayerManager.exoPlayer
            player?.seekTo((player.currentPosition - 5000).coerceAtLeast(0))
            return
        }
        if (action == "ACTION_FFWD") {
            val player = com.example.service.PlayerManager.exoPlayer
            player?.seekTo((player.currentPosition + 5000).coerceAtMost(player.duration))
            return
        }
        if (action == "ACTION_STOP") {
            val player = com.example.service.PlayerManager.exoPlayer
            player?.stop()
            player?.clearMediaItems()
            
            // Re-render widget to show Folders mode
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
            appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetManager.getAppWidgetIds(componentName), R.id.widget_list)
            
            val intentUpdate = Intent(context, MediaWidgetProvider::class.java)
            intentUpdate.action = AppWidgetManager.ACTION_APPWIDGET_UPDATE
            intentUpdate.putExtra(AppWidgetManager.EXTRA_APPWIDGET_IDS, appWidgetManager.getAppWidgetIds(componentName))
            context.sendBroadcast(intentUpdate)
            return
        }
        
        if (action == "ACTION_BACK_FOLDER") {
            val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
            prefs.edit().remove("folder_id").remove("search_query").apply()
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
            appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetManager.getAppWidgetIds(componentName), R.id.widget_list)
            
            val intentUpdate = Intent(context, MediaWidgetProvider::class.java)
            intentUpdate.action = AppWidgetManager.ACTION_APPWIDGET_UPDATE
            intentUpdate.putExtra(AppWidgetManager.EXTRA_APPWIDGET_IDS, appWidgetManager.getAppWidgetIds(componentName))
            context.sendBroadcast(intentUpdate)
            return
        }
        
        if (action == "ACTION_OPEN_APP") {"""

content = content.replace(receive_old, receive_new)

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
    f.write(content)
print("Updated MediaWidgetProvider")
