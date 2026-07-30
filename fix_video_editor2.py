import re
with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

target = """                            val intent = android.content.Intent(context, com.example.EditMediaActivity::class.java).apply {
                                action = android.content.Intent.ACTION_EDIT
                                setDataAndType(Uri.parse(newUri), "video/*")
                            }"""

replacement = """                            val intent = android.content.Intent(context, com.example.MainActivity::class.java).apply {
                                action = android.content.Intent.ACTION_EDIT
                                setDataAndType(Uri.parse(newUri), "video/*")
                            }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)
print("Replaced")
