import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

old_block = """                val previewModifier = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) {
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
                }
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
                        modifier = previewModifier.graphicsLayer {
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
                    Box(modifier = previewModifier.background(Color.Black))
                }"""

new_block = """                val density = androidx.compose.ui.platform.LocalDensity.current
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

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Block not found!")
