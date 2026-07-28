import re

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

# Add logging to onUpdate
content = content.replace(
    "override fun onUpdate(context: Context, appWidgetManager: AppWidgetManager, appWidgetIds: IntArray) {\n        try {",
    """override fun onUpdate(context: Context, appWidgetManager: AppWidgetManager, appWidgetIds: IntArray) {
        com.example.LogKeeper.log("onUpdate started for ${appWidgetIds.size} widgets", "MediaWidgetProvider")
        try {"""
)

# Add logging to updateAppWidget
content = content.replace(
    "private fun updateAppWidget(context: Context, appWidgetManager: AppWidgetManager, appWidgetId: Int) {",
    """private fun updateAppWidget(context: Context, appWidgetManager: AppWidgetManager, appWidgetId: Int) {
        com.example.LogKeeper.log("updateAppWidget started for widgetId $appWidgetId", "MediaWidgetProvider")
        try {"""
)

content = content.replace(
    "appWidgetManager.updateAppWidget(appWidgetId, views)",
    """appWidgetManager.updateAppWidget(appWidgetId, views)
            com.example.LogKeeper.log("updateAppWidget completed for widgetId $appWidgetId", "MediaWidgetProvider")
        } catch (e: Exception) {
            com.example.LogKeeper.logError("MediaWidgetProvider", "Error in updateAppWidget for widgetId $appWidgetId", e)
        }"""
)

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
    f.write(content)
