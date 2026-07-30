with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

target = """        // Intents for playback controls
        views.setOnClickPendingIntent(R.id.widget_btn_prev, getPendingIntent(context, "ACTION_PREV"))
        views.setOnClickPendingIntent(R.id.widget_btn_play, getPendingIntent(context, "ACTION_PLAY_PAUSE"))
        views.setOnClickPendingIntent(R.id.widget_btn_next, getPendingIntent(context, "ACTION_NEXT"))
        views.setOnClickPendingIntent(R.id.widget_btn_loop, getPendingIntent(context, "ACTION_LOOP"))
        views.setOnClickPendingIntent(R.id.widget_btn_shuffle, getPendingIntent(context, "ACTION_SHUFFLE"))
        views.setOnClickPendingIntent(R.id.widget_btn_refresh, getPendingIntent(context, "ACTION_REFRESH"))

        val searchIntent = Intent(context, MainActivity::class.java).apply {
            action = "ACTION_SEARCH"
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        val searchPendingIntent = PendingIntent.getActivity(
            context,
            2,
            searchIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        views.setOnClickPendingIntent(R.id.widget_btn_search, searchPendingIntent)"""

replacement = """        // Top bar intents
        views.setOnClickPendingIntent(R.id.widget_btn_pip, getPendingIntent(context, "ACTION_PIP"))
        views.setOnClickPendingIntent(R.id.widget_btn_expand, getPendingIntent(context, "ACTION_OPEN_APP"))
        views.setOnClickPendingIntent(R.id.widget_btn_refresh, getPendingIntent(context, "ACTION_REFRESH"))
        
        // Intents for playback controls
        views.setOnClickPendingIntent(R.id.widget_btn_prev, getPendingIntent(context, "ACTION_PREV"))
        views.setOnClickPendingIntent(R.id.widget_btn_play, getPendingIntent(context, "ACTION_PLAY_PAUSE"))
        views.setOnClickPendingIntent(R.id.widget_btn_next, getPendingIntent(context, "ACTION_NEXT"))
        views.setOnClickPendingIntent(R.id.widget_btn_loop, getPendingIntent(context, "ACTION_LOOP"))
        views.setOnClickPendingIntent(R.id.widget_btn_shuffle, getPendingIntent(context, "ACTION_SHUFFLE"))
        
        // Bottom right intents
        views.setOnClickPendingIntent(R.id.widget_btn_close, getPendingIntent(context, "ACTION_CLOSE"))
        views.setOnClickPendingIntent(R.id.widget_btn_miniplayer, getPendingIntent(context, "ACTION_MINIPLAYER"))
        
        val searchIntent = Intent(context, MainActivity::class.java).apply {
            action = "ACTION_SEARCH"
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        val searchPendingIntent = PendingIntent.getActivity(
            context,
            2,
            searchIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        views.setOnClickPendingIntent(R.id.widget_btn_search, searchPendingIntent)"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
