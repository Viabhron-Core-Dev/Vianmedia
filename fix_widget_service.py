import re

with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "r") as f:
    content = f.read()

target = "if (player != null && !player.currentTimeline.isEmpty && player.isPlaying) {"
replacement = "if (player != null && !player.currentTimeline.isEmpty) {"

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
