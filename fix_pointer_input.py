with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "r") as f:
    content = f.read()

target = ".pointerInput(Unit) {"
replacement = ".pointerInput(item.id, index) {"
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "w") as f:
    f.write(content)
