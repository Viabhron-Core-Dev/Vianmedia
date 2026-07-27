with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

target = ".background(androidx.compose.ui.graphics.Color.White)"
replacement = ".background(MaterialTheme.colorScheme.surface)"
content = content.replace(target, replacement)

# Fix the first one back to copy(alpha=0.95f)
content = content.replace(".background(MaterialTheme.colorScheme.surface)", ".background(MaterialTheme.colorScheme.surface.copy(alpha = 0.95f))", 1)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
