import re

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

# Remove old buttons and add new buttons
new_intents = """        // Intents for playback controls
        views.setOnClickPendingIntent(R.id.widget_btn_prev, getPendingIntent(context, "ACTION_PREV"))
        views.setOnClickPendingIntent(R.id.widget_btn_play, getPendingIntent(context, "ACTION_PLAY_PAUSE"))
        views.setOnClickPendingIntent(R.id.widget_btn_next, getPendingIntent(context, "ACTION_NEXT"))
        views.setOnClickPendingIntent(R.id.widget_btn_open_app, getPendingIntent(context, "ACTION_OPEN_APP"))
        views.setOnClickPendingIntent(R.id.widget_btn_miniplayer, getPendingIntent(context, "ACTION_MINIPLAYER"))
        views.setOnClickPendingIntent(R.id.widget_btn_close, getPendingIntent(context, "ACTION_CLOSE"))
"""
content = re.sub(r'        // Intents for playback controls.*?views\.setOnClickPendingIntent\(R\.id\.widget_btn_mode, getPendingIntent\(context, "ACTION_TOGGLE_MODE"\)\)', new_intents, content, flags=re.DOTALL)

# Handle ACTION_OPEN_APP in onReceive to launch main activity
on_receive_app = """        if (action == "ACTION_OPEN_APP") {
            val appIntent = Intent(context, MainActivity::class.java).apply {
                action = "com.example.ACTION_OPEN_PLAYER"
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            context.startActivity(appIntent)
        } else if (action in listOf("ACTION_PLAY_PAUSE", "ACTION_PREV", "ACTION_NEXT", "ACTION_MINIPLAYER", "ACTION_CLOSE")) {"""
content = re.sub(r'        if \(action == "ACTION_TOGGLE_MODE"\) \{.*?\} else if \(action in listOf\("ACTION_PLAY_PAUSE", "ACTION_PREV", "ACTION_NEXT", "ACTION_LOOP", "ACTION_SHUFFLE"\)\) \{', on_receive_app, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
    f.write(content)
