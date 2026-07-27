with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

target = ".background(MaterialTheme.colorScheme.surface.copy(alpha = 0.95f))"
replacement = ".background(MaterialTheme.colorScheme.background)"
content = content.replace(target, replacement)

target2 = ".background(MaterialTheme.colorScheme.surface)"
replacement2 = ".background(MaterialTheme.colorScheme.surface)" # already surface, maybe leave it, or change to background?
# Top bar can be surface (white) or background (light blue)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
