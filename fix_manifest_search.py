import re
with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

target = """        <receiver android:name=".widget.MediaWidgetProvider" android:exported="true">"""
replacement = """        <activity
            android:name=".widget.WidgetSearchActivity"
            android:theme="@style/Theme.Transparent"
            android:excludeFromRecents="true"
            android:exported="false" />

        <receiver android:name=".widget.MediaWidgetProvider" android:exported="true">"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/AndroidManifest.xml", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
