with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

target = ".background(MaterialTheme.colorScheme.surface.copy(alpha = 0.95f))"
replacement = ".background(androidx.compose.ui.graphics.Color.White)"
content = content.replace(target, replacement)

target2 = ".background(MaterialTheme.colorScheme.surface)"
replacement2 = ".background(androidx.compose.ui.graphics.Color.White)"
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
