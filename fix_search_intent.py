with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

target = """        val searchIntent = Intent(context, MainActivity::class.java).apply {
            action = "ACTION_SEARCH"
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }"""

replacement = """        val searchIntent = Intent(context, WidgetSearchActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
