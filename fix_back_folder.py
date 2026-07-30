with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

target = """                if (widgetAction == "OPEN_FOLDER") {
                    val folderId = intent.getStringExtra("FOLDER_ID")
                    prefs.edit().putString("folder_id", folderId).apply()
                } else {
                    prefs.edit().putString("folder_id", null).apply()
                }"""

replacement = """                if (widgetAction == "OPEN_FOLDER") {
                    val folderId = intent.getStringExtra("FOLDER_ID")
                    prefs.edit().putString("folder_id", folderId).apply()
                } else {
                    prefs.edit().putString("folder_id", null).putString("search_query", null).apply()
                }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
