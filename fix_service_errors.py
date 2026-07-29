import re

with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    content = f.read()

# Fix isInitialized
content = content.replace(
    '        if (::widgetCommandReceiver.isInitialized) {\n            unregisterReceiver(widgetCommandReceiver)\n        }',
    '        try { unregisterReceiver(widgetCommandReceiver) } catch (e: Exception) {}'
)

# Fix widget_progress
content = re.sub(r'                val duration = player\.duration\.coerceAtLeast\(0\)\n                val position = player\.currentPosition\.coerceAtLeast\(0\)\n                views\.setProgressBar\(com\.example\.R\.id\.widget_progress, duration\.toInt\(\), position\.toInt\(\), false\)\n', '', content)

with open("app/src/main/java/com/example/service/PlaybackService.kt", "w") as f:
    f.write(content)
