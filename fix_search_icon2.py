with open("app/src/main/java/com/example/widget/WidgetSearchActivity.kt", "r") as f:
    content = f.read()

target = "Icon(androidx.compose.material.icons.Icons.Filled.Search, \"Search\")"
replacement = "Icon(androidx.compose.material.icons.filled.Search, \"Search\")"

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/widget/WidgetSearchActivity.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
