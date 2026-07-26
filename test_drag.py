with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "r") as f:
    content = f.read()

target = """                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .onSizeChanged { size ->
                                itemHeightPx = size.height.toFloat()
                            }
                            .zIndex(if (isDragging) 1f else 0f)
                            .graphicsLayer {
                                translationY = if (isDragging) targetOffset else animatedOffset
                            }"""
replacement = """                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .onSizeChanged { size ->
                                itemHeightPx = size.height.toFloat()
                            }
                            .animateItem()
                            .zIndex(if (isDragging) 1f else 0f)
                            .graphicsLayer {
                                translationY = if (isDragging) targetOffset else animatedOffset
                            }"""
content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "w") as f:
    f.write(content)
