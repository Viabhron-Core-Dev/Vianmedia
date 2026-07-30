with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

old_block = """                        modifier = previewModifier.graphicsLayer {
                            clip = true
                            rotationZ = editState.rotateConfig.toFloat()
                            var rotScale = 1f
                            if (editState.rotateConfig == 90 || editState.rotateConfig == 270) {
                                rotScale = minOf(size.width / size.height, size.height / size.width)
                                scaleX = rotScale
                                scaleY = rotScale
                            }
                            if (currentTool != VideoEditorTool.CROP && editState.cropRect == "Custom") {
                                val cw = editState.cropRight - editState.cropLeft
                                val ch = editState.cropBottom - editState.cropTop
                                if (cw > 0 && ch > 0) {
                                    scaleX = (1f / cw) * rotScale
                                    scaleY = (1f / ch) * rotScale
                                    val cx = (editState.cropLeft + editState.cropRight) / 2f
                                    val cy = (editState.cropTop + editState.cropBottom) / 2f
                                    translationX = (0.5f - cx) * size.width * scaleX
                                    translationY = (0.5f - cy) * size.height * scaleY
                                }
                            } else if (currentTool != VideoEditorTool.CROP && editState.cropRect == "Center Crop") {
                                val s = maxOf(size.width, size.height)
                                scaleX = (s / size.width) * rotScale
                                scaleY = (s / size.height) * rotScale
                            }
                        }"""

new_block = """                        modifier = previewModifier
                            .androidx.compose.ui.layout.layout { measurable, constraints ->
                                if (editState.rotateConfig == 90 || editState.rotateConfig == 270) {
                                    val swappedConstraints = androidx.compose.ui.unit.Constraints(
                                        minWidth = constraints.minHeight,
                                        maxWidth = if (constraints.hasBoundedHeight) constraints.maxHeight else androidx.compose.ui.unit.Constraints.Infinity,
                                        minHeight = constraints.minWidth,
                                        maxHeight = if (constraints.hasBoundedWidth) constraints.maxWidth else androidx.compose.ui.unit.Constraints.Infinity
                                    )
                                    val placeable = measurable.measure(swappedConstraints)
                                    layout(placeable.height, placeable.width) {
                                        placeable.place(
                                            x = (placeable.height - placeable.width) / 2,
                                            y = (placeable.width - placeable.height) / 2
                                        )
                                    }
                                } else {
                                    val placeable = measurable.measure(constraints)
                                    layout(placeable.width, placeable.height) {
                                        placeable.place(0, 0)
                                    }
                                }
                            }
                            .graphicsLayer {
                                clip = true
                                rotationZ = editState.rotateConfig.toFloat()
                                if (currentTool != VideoEditorTool.CROP && editState.cropRect == "Custom") {
                                    val cw = editState.cropRight - editState.cropLeft
                                    val ch = editState.cropBottom - editState.cropTop
                                    if (cw > 0 && ch > 0) {
                                        scaleX = (1f / cw)
                                        scaleY = (1f / ch)
                                        val cx = (editState.cropLeft + editState.cropRight) / 2f
                                        val cy = (editState.cropTop + editState.cropBottom) / 2f
                                        translationX = (0.5f - cx) * size.width * scaleX
                                        translationY = (0.5f - cy) * size.height * scaleY
                                    }
                                } else if (currentTool != VideoEditorTool.CROP && editState.cropRect == "Center Crop") {
                                    val s = maxOf(size.width, size.height)
                                    scaleX = (s / size.width)
                                    scaleY = (s / size.height)
                                }
                            }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Fixed preview logic 2")
else:
    print("Could not find block 2")
