with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    content = f.read()

content = content.replace("appWidgetManager.updateAppWidget(appWidgetId, views)", "appWidgetManager.partiallyUpdateAppWidget(appWidgetId, views)")

with open("app/src/main/java/com/example/service/PlaybackService.kt", "w") as f:
    f.write(content)
print("Replaced")
