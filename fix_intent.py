import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace intent logic
old_intent = """              } else if (currentIntent?.action == android.content.Intent.ACTION_VIEW) {"""
new_intent = """              } else if (currentIntent?.action == android.content.Intent.ACTION_VIEW || currentIntent?.action == "edit") {"""
content = content.replace(old_intent, new_intent)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

print("Fixed intent logic in MainActivity")
