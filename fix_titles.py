import re

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

old_titles = """            when (currentMode) {
                "root" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Library")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.GONE)
                }
                "current" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Current")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
                "folders" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Folders")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
                "folder_items" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Folder Items")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
                "playlists" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Playlists")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
            }"""

new_titles = """            when (currentMode) {
                "root" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Library")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.GONE)
                }
                "current" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Now Playing")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
                "folders" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Folders")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
                "folder_items" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Folder Items")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
                "playlists" -> {
                    views.setTextViewText(R.id.widget_explorer_title, "Saved Playlists")
                    views.setViewVisibility(R.id.widget_btn_back, android.view.View.VISIBLE)
                }
            }"""

content = content.replace(old_titles, new_titles)

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
    f.write(content)
print("Updated titles")
