import re

with open("app/src/main/res/layout/widget_media.xml", "r") as f:
    content = f.read()

replacements = {
    "@android:drawable/ic_popup_sync": "@drawable/ic_widget_refresh",
    "@android:drawable/ic_menu_gallery": "@drawable/ic_widget_pip",
    "@android:drawable/ic_menu_search": "@drawable/ic_widget_search",
    "@android:drawable/ic_menu_crop": "@drawable/ic_widget_miniplayer",
    "@android:drawable/ic_menu_close_clear_cancel": "@drawable/ic_widget_close",
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open("app/src/main/res/layout/widget_media.xml", "w") as f:
    f.write(content)

print("Updated widget_media.xml")
