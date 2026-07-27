with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "r") as f:
    content = f.read()

target = """                            .graphicsLayer {
                                translationY = if (isDragging) targetOffset else animatedOffset
                            }"""

replacement = """                            .graphicsLayer {
                                translationY = if (draggedItemIndex != null) {
                                    if (isDragging) targetOffset else animatedOffset
                                } else {
                                    0f
                                }
                            }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "w") as f:
    f.write(content)
