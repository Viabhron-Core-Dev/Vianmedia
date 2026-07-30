with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()
import re
match = re.search(r'if \(action == "ACTION_CLOSE"\).*?else if \(action == "ACTION_MINIPLAYER"\).*?\}', content, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Not found")
