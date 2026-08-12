import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = """                        val internalRatio = if (editState.rotateConfig % 180 != 0) 1f / effectiveRatio else effectiveRatio
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .aspectRatio(internalRatio)
                                .graphicsLayer {
                                    rotationZ = editState.rotateConfig.toFloat()
                                },
                            contentAlignment = Alignment.Center
                        ) {"""

replacement = """                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .androidx.compose.ui.layout.layout { measurable, constraints ->
                                    if (editState.rotateConfig % 180 != 0) {
                                        val placeable = measurable.measure(
                                            androidx.compose.ui.unit.Constraints.fixed(constraints.maxHeight, constraints.maxWidth)
                                        )
                                        layout(constraints.maxWidth, constraints.maxHeight) {
                                            val x = (constraints.maxWidth - placeable.width) / 2
                                            val y = (constraints.maxHeight - placeable.height) / 2
                                            placeable.place(x, y)
                                        }
                                    } else {
                                        val placeable = measurable.measure(constraints)
                                        layout(placeable.width, placeable.height) {
                                            placeable.place(0, 0)
                                        }
                                    }
                                }
                                .graphicsLayer {
                                    rotationZ = editState.rotateConfig.toFloat()
                                },
                            contentAlignment = Alignment.Center
                        ) {"""

if target in content:
    content = content.replace(target, replacement)
    print("Success layout")
else:
    print("Target not found")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
