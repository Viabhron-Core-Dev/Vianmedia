import re
with open("app/src/main/res/layout/widget_media.xml", "r") as f:
    content = f.read()

content = content.replace('android:divider="@drawable/widget_divider"', 'android:divider="@null"')
content = content.replace('android:dividerHeight="1dp"', 'android:dividerHeight="0dp"')

with open("app/src/main/res/layout/widget_media.xml", "w") as f:
    f.write(content)
print("Removed dividers from ListView")
