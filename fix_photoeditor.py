import re

with open("app/src/main/java/com/example/ui/screens/PhotoEditorScreen.kt", "r") as f:
    content = f.read()

old_cb = """            onStartCompression = { uris, w, h ->"""
new_cb = """            onStartCompression = { uris, w, h, q, f ->"""

content = content.replace(old_cb, new_cb)

with open("app/src/main/java/com/example/ui/screens/PhotoEditorScreen.kt", "w") as f:
    f.write(content)
