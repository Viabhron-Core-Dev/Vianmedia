with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

content = content.replace(
    '        views.setOnClickPendingIntent(R.id.widget_btn_open_app, getPendingIntent(context, "ACTION_OPEN_APP"))',
    '        views.setOnClickPendingIntent(R.id.widget_btn_open_app, getPendingIntent(context, "ACTION_OPEN_APP"))\n        views.setOnClickPendingIntent(R.id.widget_btn_pip, getPendingIntent(context, "ACTION_PIP"))'
)

new_action = """        } else if (action == "ACTION_PIP") {
            val appIntent = android.content.Intent(context, com.example.MainActivity::class.java).apply {
                this.action = "com.example.ACTION_START_PIP"
                flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            context.startActivity(appIntent)
        } else if (action in listOf("ACTION_PLAY_PAUSE","""

content = content.replace('        } else if (action in listOf("ACTION_PLAY_PAUSE",', new_action)

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
    f.write(content)
