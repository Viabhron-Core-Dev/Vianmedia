import sys

with open('app/src/main/java/com/example/widget/MediaWidgetProvider.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val isMediaCommand = action in listOf("ACTION_PLAY_PAUSE", "ACTION_PREV", "ACTION_NEXT", "ACTION_LOOP", "ACTION_SHUFFLE", "ACTION_MINIPLAYER", "ACTION_CLOSE") ||',
    'val isMediaCommand = action in listOf("ACTION_PLAY_PAUSE", "ACTION_PREV", "ACTION_NEXT", "ACTION_LOOP", "ACTION_SHUFFLE", "ACTION_MINIPLAYER", "ACTION_CLOSE", "ACTION_PIP") ||'
)

new_action = """                    } else if (action == "ACTION_PIP") {
                        val serviceIntent = Intent("com.example.ACTION_WIDGET_COMMAND")
                        serviceIntent.setPackage(context.packageName)
                        serviceIntent.putExtra("command", "ACTION_VIDEO_OVERLAY")
                        context.sendBroadcast(serviceIntent)
"""
content = content.replace(
    '} else if (action == "ACTION_PLAY_ITEM") {',
    new_action + '                    } else if (action == "ACTION_PLAY_ITEM") {'
)

with open('app/src/main/java/com/example/widget/MediaWidgetProvider.kt', 'w') as f:
    f.write(content)
