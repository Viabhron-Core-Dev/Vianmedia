import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

old_canvas_block = """                if (currentTool == VideoEditorTool.CROP && editState.cropRect == "Custom") {
                    var resizeCorner by remember { mutableIntStateOf(0) }
                    Canvas(modifier = Modifier.fillMaxSize().pointerInput(Unit) {
                        detectDragGestures(
                            onDragStart = { offset ->
                                if (videoWidth == 0 || videoHeight == 0) return@detectDragGestures
                                val canvasAspect = size.width.toFloat() / size.height.toFloat()
                                val effectiveVideoWidth = videoWidth
                                val effectiveVideoHeight = videoHeight
                                val videoAspect = effectiveVideoWidth.toFloat() / effectiveVideoHeight.toFloat()
                                var drawWidth = size.width.toFloat()
                                var drawHeight = size.height.toFloat()
                                if (videoAspect > canvasAspect) {
                                    drawHeight = size.width / videoAspect
                                } else {
                                    drawWidth = size.height * videoAspect
                                }
                                val left = (size.width - drawWidth) / 2f
                                val top = (size.height - drawHeight) / 2f
                                
                                val cL = left + editState.cropLeft * drawWidth
                                val cT = top + editState.cropTop * drawHeight
                                val cR = left + editState.cropRight * drawWidth
                                val cB = top + editState.cropBottom * drawHeight
                                
                                val touchRadius = 60f
                                if (abs(offset.x - cL) < touchRadius && abs(offset.y - cT) < touchRadius) resizeCorner = 1
                                else if (abs(offset.x - cR) < touchRadius && abs(offset.y - cT) < touchRadius) resizeCorner = 2
                                else if (abs(offset.x - cL) < touchRadius && abs(offset.y - cB) < touchRadius) resizeCorner = 3
                                else if (abs(offset.x - cR) < touchRadius && abs(offset.y - cB) < touchRadius) resizeCorner = 4
                                else if (offset.x > cL && offset.x < cR && offset.y > cT && offset.y < cB) resizeCorner = 5
                            },
                            onDrag = { change, dragAmount ->
                                change.consume()
                                if (videoWidth == 0 || videoHeight == 0) return@detectDragGestures
                                val canvasAspect = size.width.toFloat() / size.height.toFloat()
                                val effectiveVideoWidth = videoWidth
                                val effectiveVideoHeight = videoHeight
                                val videoAspect = effectiveVideoWidth.toFloat() / effectiveVideoHeight.toFloat()
                                var drawWidth = size.width.toFloat()
                                var drawHeight = size.height.toFloat()
                                if (videoAspect > canvasAspect) {
                                    drawHeight = size.width / videoAspect
                                } else {
                                    drawWidth = size.height * videoAspect
                                }
                                val dx = dragAmount.x / drawWidth
                                val dy = dragAmount.y / drawHeight
                                
                                var nL = editState.cropLeft
                                var nT = editState.cropTop
                                var nR = editState.cropRight
                                var nB = editState.cropBottom
                                
                                when (resizeCorner) {
                                    5 -> {
                                        nL = (nL + dx).coerceIn(0f, 1f - (nR - editState.cropLeft))
                                        nR = nL + (editState.cropRight - editState.cropLeft)
                                        nT = (nT + dy).coerceIn(0f, 1f - (nB - editState.cropTop))
                                        nB = nT + (editState.cropBottom - editState.cropTop)
                                    }
                                    1 -> {
                                        nL = (nL + dx).coerceIn(0f, nR - 0.05f)
                                        nT = (nT + dy).coerceIn(0f, nB - 0.05f)
                                    }
                                    2 -> {
                                        nR = (nR + dx).coerceIn(nL + 0.05f, 1f)
                                        nT = (nT + dy).coerceIn(0f, nB - 0.05f)
                                    }
                                    3 -> {
                                        nL = (nL + dx).coerceIn(0f, nR - 0.05f)
                                        nB = (nB + dy).coerceIn(nT + 0.05f, 1f)
                                    }
                                    4 -> {
                                        nR = (nR + dx).coerceIn(nL + 0.05f, 1f)
                                        nB = (nB + dy).coerceIn(nT + 0.05f, 1f)
                                    }
                                }
                                editState = editState.copy(cropLeft = nL, cropTop = nT, cropRight = nR, cropBottom = nB)
                            },
                            onDragEnd = { resizeCorner = 0 },
                            onDragCancel = { resizeCorner = 0 }
                        )
                    }) {
                        if (videoWidth == 0 || videoHeight == 0) return@Canvas
                        val canvasAspect = size.width / size.height
                        val videoAspect = videoWidth.toFloat() / videoHeight.toFloat()
                        var drawWidth = size.width
                        var drawHeight = size.height
                        if (videoAspect > canvasAspect) {
                            drawHeight = size.width / videoAspect
                        } else {
                            drawWidth = size.height * videoAspect
                        }
                        val left = (size.width - drawWidth) / 2f
                        val top = (size.height - drawHeight) / 2f
                        
                        val cL = left + editState.cropLeft * drawWidth
                        val cT = top + editState.cropTop * drawHeight
                        val cR = left + editState.cropRight * drawWidth
                        val cB = top + editState.cropBottom * drawHeight
                        
                        drawRect(color = Color.Black.copy(alpha = 0.5f), topLeft = Offset(left, top), size = Size(drawWidth, cT - top))
                        drawRect(color = Color.Black.copy(alpha = 0.5f), topLeft = Offset(left, cB), size = Size(drawWidth, top + drawHeight - cB))
                        drawRect(color = Color.Black.copy(alpha = 0.5f), topLeft = Offset(left, cT), size = Size(cL - left, cB - cT))
                        drawRect(color = Color.Black.copy(alpha = 0.5f), topLeft = Offset(cR, cT), size = Size(left + drawWidth - cR, cB - cT))
                        
                        drawRect(color = Color.White, topLeft = Offset(cL, cT), size = Size(cR - cL, cB - cT), style = Stroke(width = 5f))
                        
                        val cornerLen = 40f
                        drawLine(Color.Green, Offset(cL, cT), Offset(cL + cornerLen, cT), 12f)
                        drawLine(Color.Green, Offset(cL, cT), Offset(cL, cT + cornerLen), 12f)
                        
                        drawLine(Color.Green, Offset(cR, cT), Offset(cR - cornerLen, cT), 12f)
                        drawLine(Color.Green, Offset(cR, cT), Offset(cR, cT + cornerLen), 12f)
                        
                        drawLine(Color.Green, Offset(cL, cB), Offset(cL + cornerLen, cB), 12f)
                        drawLine(Color.Green, Offset(cL, cB), Offset(cL, cB - cornerLen), 12f)
                        
                        drawLine(Color.Green, Offset(cR, cB), Offset(cR - cornerLen, cB), 12f)
                        drawLine(Color.Green, Offset(cR, cB), Offset(cR, cB - cornerLen), 12f)
                    }
                }"""

new_canvas_block = """                val showCropOverlay = (currentTool == VideoEditorTool.CROP && editState.cropRect != "None") || 
                                      (currentTool == VideoEditorTool.ASPECT_RATIO && editState.aspectRatio != "Original")
                
                if (showCropOverlay) {
                    var resizeCorner by remember { mutableIntStateOf(0) }
                    
                    val isCustom = currentTool == VideoEditorTool.CROP && editState.cropRect == "Custom"
                    
                    val effectiveVideoWidth = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) videoHeight else videoWidth
                    val effectiveVideoHeight = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) videoWidth else videoHeight
                    
                    var displayCropLeft = editState.cropLeft
                    var displayCropTop = editState.cropTop
                    var displayCropRight = editState.cropRight
                    var displayCropBottom = editState.cropBottom
                    
                    if (!isCustom && effectiveVideoHeight > 0) {
                        val videoAspect = effectiveVideoWidth.toFloat() / effectiveVideoHeight.toFloat()
                        val targetRatio = if (currentTool == VideoEditorTool.CROP && editState.cropRect == "Center Crop") {
                            1f
                        } else {
                            when (editState.aspectRatio) {
                                "16:9" -> 16f / 9f
                                "9:16" -> 9f / 16f
                                "1:1" -> 1f
                                "4:3" -> 4f / 3f
                                "21:9" -> 21f / 9f
                                else -> videoAspect
                            }
                        }
                        
                        if (videoAspect > targetRatio) {
                            val cropWidth = targetRatio / videoAspect
                            displayCropLeft = (1f - cropWidth) / 2f
                            displayCropRight = 1f - displayCropLeft
                            displayCropTop = 0f
                            displayCropBottom = 1f
                        } else {
                            val cropHeight = videoAspect / targetRatio
                            displayCropTop = (1f - cropHeight) / 2f
                            displayCropBottom = 1f - displayCropTop
                            displayCropLeft = 0f
                            displayCropRight = 1f
                        }
                    }

                    val pointerInputModifier = if (isCustom) {
                        Modifier.pointerInput(Unit) {
                            detectDragGestures(
                                onDragStart = { offset ->
                                    if (effectiveVideoWidth == 0 || effectiveVideoHeight == 0) return@detectDragGestures
                                    val canvasAspect = size.width.toFloat() / size.height.toFloat()
                                    val videoAspect = effectiveVideoWidth.toFloat() / effectiveVideoHeight.toFloat()
                                    var drawWidth = size.width.toFloat()
                                    var drawHeight = size.height.toFloat()
                                    if (videoAspect > canvasAspect) {
                                        drawHeight = size.width / videoAspect
                                    } else {
                                        drawWidth = size.height * videoAspect
                                    }
                                    val left = (size.width - drawWidth) / 2f
                                    val top = (size.height - drawHeight) / 2f
                                    
                                    val cL = left + editState.cropLeft * drawWidth
                                    val cT = top + editState.cropTop * drawHeight
                                    val cR = left + editState.cropRight * drawWidth
                                    val cB = top + editState.cropBottom * drawHeight
                                    
                                    val touchRadius = 60f
                                    if (abs(offset.x - cL) < touchRadius && abs(offset.y - cT) < touchRadius) resizeCorner = 1
                                    else if (abs(offset.x - cR) < touchRadius && abs(offset.y - cT) < touchRadius) resizeCorner = 2
                                    else if (abs(offset.x - cL) < touchRadius && abs(offset.y - cB) < touchRadius) resizeCorner = 3
                                    else if (abs(offset.x - cR) < touchRadius && abs(offset.y - cB) < touchRadius) resizeCorner = 4
                                    else if (offset.x > cL && offset.x < cR && offset.y > cT && offset.y < cB) resizeCorner = 5
                                },
                                onDrag = { change, dragAmount ->
                                    change.consume()
                                    if (effectiveVideoWidth == 0 || effectiveVideoHeight == 0) return@detectDragGestures
                                    val canvasAspect = size.width.toFloat() / size.height.toFloat()
                                    val videoAspect = effectiveVideoWidth.toFloat() / effectiveVideoHeight.toFloat()
                                    var drawWidth = size.width.toFloat()
                                    var drawHeight = size.height.toFloat()
                                    if (videoAspect > canvasAspect) {
                                        drawHeight = size.width / videoAspect
                                    } else {
                                        drawWidth = size.height * videoAspect
                                    }
                                    val dx = dragAmount.x / drawWidth
                                    val dy = dragAmount.y / drawHeight
                                    
                                    var nL = editState.cropLeft
                                    var nT = editState.cropTop
                                    var nR = editState.cropRight
                                    var nB = editState.cropBottom
                                    
                                    when (resizeCorner) {
                                        5 -> {
                                            nL = (nL + dx).coerceIn(0f, 1f - (nR - editState.cropLeft))
                                            nR = nL + (editState.cropRight - editState.cropLeft)
                                            nT = (nT + dy).coerceIn(0f, 1f - (nB - editState.cropTop))
                                            nB = nT + (editState.cropBottom - editState.cropTop)
                                        }
                                        1 -> {
                                            nL = (nL + dx).coerceIn(0f, nR - 0.05f)
                                            nT = (nT + dy).coerceIn(0f, nB - 0.05f)
                                        }
                                        2 -> {
                                            nR = (nR + dx).coerceIn(nL + 0.05f, 1f)
                                            nT = (nT + dy).coerceIn(0f, nB - 0.05f)
                                        }
                                        3 -> {
                                            nL = (nL + dx).coerceIn(0f, nR - 0.05f)
                                            nB = (nB + dy).coerceIn(nT + 0.05f, 1f)
                                        }
                                        4 -> {
                                            nR = (nR + dx).coerceIn(nL + 0.05f, 1f)
                                            nB = (nB + dy).coerceIn(nT + 0.05f, 1f)
                                        }
                                    }
                                    editState = editState.copy(cropLeft = nL, cropTop = nT, cropRight = nR, cropBottom = nB)
                                },
                                onDragEnd = { resizeCorner = 0 },
                                onDragCancel = { resizeCorner = 0 }
                            )
                        }
                    } else {
                        Modifier
                    }

                    Canvas(modifier = Modifier.fillMaxSize().then(pointerInputModifier)) {
                        if (effectiveVideoWidth == 0 || effectiveVideoHeight == 0) return@Canvas
                        val canvasAspect = size.width / size.height
                        val videoAspect = effectiveVideoWidth.toFloat() / effectiveVideoHeight.toFloat()
                        var drawWidth = size.width
                        var drawHeight = size.height
                        if (videoAspect > canvasAspect) {
                            drawHeight = size.width / videoAspect
                        } else {
                            drawWidth = size.height * videoAspect
                        }
                        val left = (size.width - drawWidth) / 2f
                        val top = (size.height - drawHeight) / 2f
                        
                        val cL = left + displayCropLeft * drawWidth
                        val cT = top + displayCropTop * drawHeight
                        val cR = left + displayCropRight * drawWidth
                        val cB = top + displayCropBottom * drawHeight
                        
                        drawRect(color = Color.Black.copy(alpha = 0.5f), topLeft = Offset(left, top), size = Size(drawWidth, cT - top))
                        drawRect(color = Color.Black.copy(alpha = 0.5f), topLeft = Offset(left, cB), size = Size(drawWidth, top + drawHeight - cB))
                        drawRect(color = Color.Black.copy(alpha = 0.5f), topLeft = Offset(left, cT), size = Size(cL - left, cB - cT))
                        drawRect(color = Color.Black.copy(alpha = 0.5f), topLeft = Offset(cR, cT), size = Size(left + drawWidth - cR, cB - cT))
                        
                        drawRect(color = Color.White, topLeft = Offset(cL, cT), size = Size(cR - cL, cB - cT), style = Stroke(width = 5f))
                        
                        if (isCustom) {
                            val cornerLen = 40f
                            drawLine(Color.Green, Offset(cL, cT), Offset(cL + cornerLen, cT), 12f)
                            drawLine(Color.Green, Offset(cL, cT), Offset(cL, cT + cornerLen), 12f)
                            
                            drawLine(Color.Green, Offset(cR, cT), Offset(cR - cornerLen, cT), 12f)
                            drawLine(Color.Green, Offset(cR, cT), Offset(cR, cT + cornerLen), 12f)
                            
                            drawLine(Color.Green, Offset(cL, cB), Offset(cL + cornerLen, cB), 12f)
                            drawLine(Color.Green, Offset(cL, cB), Offset(cL, cB - cornerLen), 12f)
                            
                            drawLine(Color.Green, Offset(cR, cB), Offset(cR - cornerLen, cB), 12f)
                            drawLine(Color.Green, Offset(cR, cB), Offset(cR, cB - cornerLen), 12f)
                        }
                    }
                }"""

if old_canvas_block in content:
    content = content.replace(old_canvas_block, new_canvas_block)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Canvas block replaced successfully.")
else:
    print("Error: Could not find old canvas block.")
