with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    content = f.read()
import re
match = re.search(r'private val widgetCommandReceiver.*?\{.*?\}(?=\n\n|\n})', content, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Not found")
