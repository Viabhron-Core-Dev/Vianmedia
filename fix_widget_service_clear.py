with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "r") as f:
    content = f.read()

target = """                if (position == 0) {
                    views.setTextViewText(R.id.widget_item_title, "[Back to Folders]")
                    val fillInIntent = Intent().putExtra("WIDGET_ACTION", "BACK_FOLDER")
                    views.setOnClickFillInIntent(R.id.widget_item_root, fillInIntent)
                }"""

replacement = """                if (position == 0) {
                    if (folderId == "search_results") {
                        views.setTextViewText(R.id.widget_item_title, "[Clear Search]")
                    } else {
                        views.setTextViewText(R.id.widget_item_title, "[Back to Folders]")
                    }
                    val fillInIntent = Intent().putExtra("WIDGET_ACTION", "BACK_FOLDER")
                    views.setOnClickFillInIntent(R.id.widget_item_root, fillInIntent)
                }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/widget/MediaWidgetService.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
