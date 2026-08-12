import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target1 = """        if (editState.rotateConfig != 0) {
            effects.add(androidx.media3.effect.ScaleAndRotateTransformation.Builder().setRotationDegrees(editState.rotateConfig.toFloat()).build())
        }"""
replacement1 = """        // Rotation is now handled via Compose Modifier for the preview
        // if (editState.rotateConfig != 0) {
        //     effects.add(androidx.media3.effect.ScaleAndRotateTransformation.Builder().setRotationDegrees(editState.rotateConfig.toFloat()).build())
        // }"""

if target1 in content:
    content = content.replace(target1, replacement1)
    print("Success 1")
    
target2 = """                Box(modifier = visualModifier, contentAlignment = Alignment.Center) {
                    if (exoPlayer != null) {
                        AndroidView("""

replacement2 = """                Box(modifier = visualModifier, contentAlignment = Alignment.Center) {
                    if (exoPlayer != null) {
                        // Inverse ratio for the internal player view so it can be rotated to fit the container
                        val internalRatio = if (editState.rotateConfig % 180 != 0) 1f / effectiveRatio else effectiveRatio
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .aspectRatio(internalRatio)
                                .androidx.compose.ui.graphics.graphicsLayer {
                                    rotationZ = editState.rotateConfig.toFloat()
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            AndroidView("""

if target2 in content:
    content = content.replace(target2, replacement2)
    print("Success 2")
    
target3 = """                            },
                            update = { view ->
                                view.resizeMode = if (editState.aspectRatio != "Original") androidx.media3.ui.AspectRatioFrameLayout.RESIZE_MODE_FILL else androidx.media3.ui.AspectRatioFrameLayout.RESIZE_MODE_FIT
                            },
                            modifier = Modifier.fillMaxSize()
                        )
                    }"""

replacement3 = """                            },
                            update = { view ->
                                view.resizeMode = if (editState.aspectRatio != "Original") androidx.media3.ui.AspectRatioFrameLayout.RESIZE_MODE_FILL else androidx.media3.ui.AspectRatioFrameLayout.RESIZE_MODE_FIT
                            },
                            modifier = Modifier.fillMaxSize()
                        )
                        }
                    }"""

if target3 in content:
    content = content.replace(target3, replacement3)
    print("Success 3")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
