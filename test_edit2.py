import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

old_modifiers_block = """                val ratio = if (editState.cropRect == "Center Crop" && currentTool != VideoEditorTool.CROP) {
                    1f
                } else {
                    when (editState.aspectRatio) {
                        "16:9" -> 16f / 9f
                        "9:16" -> 9f / 16f
                        "1:1" -> 1f
                        "4:3" -> 4f / 3f
                        "21:9" -> 21f / 9f
                        else -> if (videoWidth > 0 && videoHeight > 0) videoWidth.toFloat() / videoHeight.toFloat() else 16f/9f
                    }
                }
                val parentWidth = constraints.maxWidth.toFloat()
                val parentHeight = constraints.maxHeight.toFloat()
                
                val density = androidx.compose.ui.platform.LocalDensity.current
                val isRotated = editState.rotateConfig == 90 || editState.rotateConfig == 270
                val (visualWidth, visualHeight) = if (isRotated) {
                    val rotatedRatio = 1f / ratio
                    if (parentWidth / parentHeight > rotatedRatio) {
                        Pair(parentHeight * rotatedRatio, parentHeight)
                    } else {
                        Pair(parentWidth, parentWidth / rotatedRatio)
                    }
                } else {
                    if (parentWidth / parentHeight > ratio) {
                        Pair(parentHeight * ratio, parentHeight)
                    } else {
                        Pair(parentWidth, parentWidth / ratio)
                    }
                }
                
                val visualModifier = Modifier
                    .requiredSize(
                        width = with(density) { visualWidth.toDp() },
                        height = with(density) { visualHeight.toDp() }
                    )
                    .background(Color.DarkGray)

                val internalModifier = if (isRotated) {
                    Modifier.requiredSize(
                        width = with(density) { visualHeight.toDp() },
                        height = with(density) { visualWidth.toDp() }
                    )
                } else {
                    Modifier.fillMaxSize()
                }

                Box(modifier = visualModifier, contentAlignment = Alignment.Center) {
                    if (exoPlayer != null) {
                        AndroidView(
                            factory = { ctx ->
                                val view = android.view.LayoutInflater.from(ctx).inflate(com.example.R.layout.player_view_texture, null) as PlayerView
                                view.apply {
                                    player = exoPlayer
                                    useController = true
                                }
                            },
                            update = { view ->
                                view.resizeMode = if (ratio != null) 3 else 0
                            },
                            modifier = internalModifier.graphicsLayer {
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
                            }
                        )
                    } else {
                        Box(modifier = Modifier.fillMaxSize().background(Color.Black))
                    }
                }"""

new_modifiers_block = """                val ratio = if (videoWidth > 0 && videoHeight > 0) videoWidth.toFloat() / videoHeight.toFloat() else 16f/9f
                
                val visualModifier = Modifier
                    .fillMaxWidth()
                    .aspectRatio(ratio)
                    .background(Color.DarkGray)

                Box(modifier = visualModifier, contentAlignment = Alignment.Center) {
                    if (exoPlayer != null) {
                        AndroidView(
                            factory = { ctx ->
                                val view = android.view.LayoutInflater.from(ctx).inflate(com.example.R.layout.player_view_texture, null) as PlayerView
                                view.apply {
                                    player = exoPlayer
                                    useController = true
                                    resizeMode = androidx.media3.ui.AspectRatioFrameLayout.RESIZE_MODE_FIT
                                }
                            },
                            modifier = Modifier.fillMaxSize()
                        )
                    } else {
                        Box(modifier = Modifier.fillMaxSize().background(Color.Black))
                    }
                }"""

content = content.replace(old_modifiers_block, new_modifiers_block)

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)
