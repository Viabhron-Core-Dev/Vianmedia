with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

target = """                    // Bottom controls background
                    Box(modifier = Modifier
                        .fillMaxWidth()
                        .height(96.dp)
                        .align(Alignment.BottomCenter)
                        .background(Brush.verticalGradient(listOf(Color.Transparent, Color.Black.copy(alpha = 0.8f))))
                    )"""

replacement = """                    // Bottom controls background
                    Box(modifier = Modifier
                        .fillMaxWidth()
                        .height(180.dp)
                        .align(Alignment.BottomCenter)
                        .background(Brush.verticalGradient(listOf(Color.Transparent, Color.Black.copy(alpha = 0.9f))))
                    )"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
