with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

# Replace intents
old_intents = """        views.setOnClickPendingIntent(R.id.widget_btn_mode, getPendingIntent(context, "ACTION_TOGGLE_MODE"))"""
new_intents = """        views.setOnClickPendingIntent(R.id.widget_btn_refresh, getPendingIntent(context, "ACTION_REFRESH"))
        views.setOnClickPendingIntent(R.id.widget_btn_open_app, getPendingIntent(context, "ACTION_OPEN_APP"))
        views.setOnClickPendingIntent(R.id.widget_btn_miniplayer, getPendingIntent(context, "ACTION_MINIPLAYER"))
        views.setOnClickPendingIntent(R.id.widget_btn_pip, getPendingIntent(context, "ACTION_PIP"))
        views.setOnClickPendingIntent(R.id.widget_btn_close, getPendingIntent(context, "ACTION_CLOSE"))"""
content = content.replace(old_intents, new_intents)

# Replace action handling
old_action_toggle = """        if (action == "ACTION_TOGGLE_MODE") {
            val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
            val currentMode = prefs.getString("mode", "PLAYLIST")
            val nextMode = if (currentMode == "PLAYLIST") "FOLDERS" else "PLAYLIST"
            prefs.edit().putString("mode", nextMode).putString("folder_id", null).apply()
            
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
            appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetManager.getAppWidgetIds(componentName), R.id.widget_list)
        } else if (action == "ACTION_PIP") {"""

new_action_replace = """        if (action == "ACTION_REFRESH") {
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
            appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetManager.getAppWidgetIds(componentName), R.id.widget_list)
        } else if (action == "ACTION_OPEN_APP") {
            val appIntent = android.content.Intent(context, com.example.MainActivity::class.java).apply {
                this.action = "com.example.ACTION_OPEN_PLAYER"
                flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            context.startActivity(appIntent)
        } else if (action == "ACTION_PIP") {"""
content = content.replace(old_action_toggle, new_action_replace)

content = content.replace('        } else if (action in listOf("ACTION_PLAY_PAUSE", "ACTION_PREV", "ACTION_NEXT", "ACTION_LOOP", "ACTION_SHUFFLE")) {', '        } else if (action in listOf("ACTION_PLAY_PAUSE", "ACTION_PREV", "ACTION_NEXT", "ACTION_LOOP", "ACTION_SHUFFLE", "ACTION_MINIPLAYER", "ACTION_CLOSE")) {')

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
    f.write(content)
