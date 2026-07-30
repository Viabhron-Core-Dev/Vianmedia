with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

import re

# Replace Box with BoxWithConstraints
content = content.replace(
"""            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.background),
                contentAlignment = Alignment.Center
            ) {""",
"""            androidx.compose.foundation.layout.BoxWithConstraints(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.background),
                contentAlignment = Alignment.Center
            ) {""")

# Replace previewModifier logic
old_logic = """                val previewModifier = Modifier
                    .aspectRatio(ratio)
                    .background(Color.DarkGray)"""

new_logic = """                val parentWidth = constraints.maxWidth.toFloat()
                val parentHeight = constraints.maxHeight.toFloat()
                
                val previewModifier = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) {
                    val rotatedRatio = 1f / ratio
                    val fitWidth: Float
                    val fitHeight: Float
                    if (parentWidth / parentHeight > rotatedRatio) {
                        fitHeight = parentHeight
                        fitWidth = fitHeight * rotatedRatio
                    } else {
                        fitWidth = parentWidth
                        fitHeight = fitWidth / rotatedRatio
                    }
                    val density = androidx.compose.ui.platform.LocalDensity.current
                    Modifier
                        .requiredSize(
                            width = with(density) { fitHeight.toDp() },
                            height = with(density) { fitWidth.toDp() }
                        )
                        .background(Color.DarkGray)
                } else {
                    Modifier
                        .aspectRatio(ratio)
                        .background(Color.DarkGray)
                }"""

content = content.replace(old_logic, new_logic)

# Replace graphicsLayer
old_gl = """                        modifier = previewModifier.graphicsLayer {
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
                                // Center Crop is effectively a 1:1 ratio. If they don't have aspect ratio 1:1 selected, we simulate it
                                // by scaling the shorter dimension. Actually, ExoPlayer resizeMode handles this if we just let it.
                            }
                        }"""

new_gl = """                        modifier = previewModifier.graphicsLayer {
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
                            }
                        }"""

if old_gl in content:
    content = content.replace(old_gl, new_gl)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Fixed layout math perfectly!")
else:
    print("Could not find graphicsLayer block")
