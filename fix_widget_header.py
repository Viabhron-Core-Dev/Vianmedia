import re
with open("app/src/main/res/layout/widget_media.xml", "r") as f:
    content = f.read()

header_block = """    <LinearLayout
        android:id="@+id/widget_explorer_header"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:padding="8dp">"""

new_header_block = """    <LinearLayout
        android:id="@+id/widget_explorer_header"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:paddingTop="8dp"
        android:paddingBottom="8dp"
        android:paddingStart="16dp"
        android:paddingEnd="16dp">"""
content = content.replace(header_block, new_header_block)

with open("app/src/main/res/layout/widget_media.xml", "w") as f:
    f.write(content)
print("Adjusted widget header")
