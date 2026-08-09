import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = """                            // For join video, we scale it to match the target or fallback to 1280x720
                            val fw = if (res != "Original") targetW else 1280
                            val fh = if (res != "Original") targetH else 720"""

replacement = """                            // For join video, we scale it to match the target or fallback to 1280x720
                            val parts2 = if (res != "Original") res.split("x") else listOf("1280", "720")
                            val fw = parts2[0].toInt()
                            val fh = parts2[1].toInt()"""

if target in content:
    content = content.replace(target, replacement)
    print("Success 1")
else:
    print("Failed 1")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
