import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

# Let's inspect the code around AndroidView
match = re.search(r'(val previewModifier.*?if \(exoPlayer != null\) \{)', content, re.DOTALL)
if match:
    print("Found previewModifier!")
    print(match.group(1)[:500])
else:
    print("Not found")
