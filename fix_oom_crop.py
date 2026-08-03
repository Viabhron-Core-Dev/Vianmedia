import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

# Fix LaunchedEffect for video effects to avoid OOM
old_effects = """    LaunchedEffect(editState.rotateConfig, editState.cropRect, editState.cropLeft, editState.cropRight, editState.cropTop, editState.cropBottom, editState.aspectRatio, currentTool) {
        val effects = mutableListOf<androidx.media3.common.Effect>()
        
        if (editState.rotateConfig != 0) {
            effects.add(androidx.media3.effect.ScaleAndRotateTransformation.Builder().setRotationDegrees(editState.rotateConfig.toFloat()).build())
        }
        
        if (currentTool != VideoEditorTool.CROP) {
            if (editState.cropRect == "Custom") {
                val cw = editState.cropRight - editState.cropLeft
                val ch = editState.cropBottom - editState.cropTop
                if (cw > 0 && ch > 0) {
                    val left = editState.cropLeft * 2f - 1f
                    val right = editState.cropRight * 2f - 1f
                    val top = 1f - editState.cropTop * 2f
                    val bottom = 1f - editState.cropBottom * 2f
                    effects.add(androidx.media3.effect.Crop(left, right, bottom, top))
                }
            }
            
            if (editState.aspectRatio != "Original" && editState.aspectRatio != "Center Crop") {
                val ratioFloat = when (editState.aspectRatio) {
                    "16:9" -> 16f / 9f
                    "9:16" -> 9f / 16f
                    "1:1" -> 1f
                    "4:3" -> 4f / 3f
                    "21:9" -> 21f / 9f
                    else -> 1f
                }
                effects.add(androidx.media3.effect.Presentation.createForAspectRatio(ratioFloat, androidx.media3.effect.Presentation.LAYOUT_SCALE_TO_FIT_WITH_CROP))
            }
        }
        
        exoPlayer?.setVideoEffects(effects)
    }"""

new_effects = """    val cropLeftKey = if (currentTool == VideoEditorTool.CROP) 0f else editState.cropLeft
    val cropRightKey = if (currentTool == VideoEditorTool.CROP) 0f else editState.cropRight
    val cropTopKey = if (currentTool == VideoEditorTool.CROP) 0f else editState.cropTop
    val cropBottomKey = if (currentTool == VideoEditorTool.CROP) 0f else editState.cropBottom

    LaunchedEffect(editState.rotateConfig, editState.cropRect, cropLeftKey, cropRightKey, cropTopKey, cropBottomKey, editState.aspectRatio, currentTool) {
        val effects = mutableListOf<androidx.media3.common.Effect>()
        
        if (editState.rotateConfig != 0) {
            effects.add(androidx.media3.effect.ScaleAndRotateTransformation.Builder().setRotationDegrees(editState.rotateConfig.toFloat()).build())
        }
        
        if (currentTool != VideoEditorTool.CROP) {
            if (editState.cropRect == "Center Crop") {
                effects.add(androidx.media3.effect.Presentation.createForAspectRatio(1f, androidx.media3.effect.Presentation.LAYOUT_SCALE_TO_FIT_WITH_CROP))
            } else if (editState.cropRect == "Custom") {
                val cw = editState.cropRight - editState.cropLeft
                val ch = editState.cropBottom - editState.cropTop
                if (cw > 0 && ch > 0) {
                    val left = editState.cropLeft * 2f - 1f
                    val right = editState.cropRight * 2f - 1f
                    val top = 1f - editState.cropTop * 2f
                    val bottom = 1f - editState.cropBottom * 2f
                    effects.add(androidx.media3.effect.Crop(left, right, bottom, top))
                }
            }
            
            if (editState.aspectRatio != "Original" && editState.cropRect != "Center Crop") {
                val ratioFloat = when (editState.aspectRatio) {
                    "16:9" -> 16f / 9f
                    "9:16" -> 9f / 16f
                    "1:1" -> 1f
                    "4:3" -> 4f / 3f
                    "21:9" -> 21f / 9f
                    else -> 1f
                }
                effects.add(androidx.media3.effect.Presentation.createForAspectRatio(ratioFloat, androidx.media3.effect.Presentation.LAYOUT_SCALE_TO_FIT_WITH_CROP))
            }
        }
        
        exoPlayer?.setVideoEffects(effects)
    }"""

content = content.replace(old_effects, new_effects)

# Fix LaunchedEffect for timeline polling to avoid OOM
old_poll = """                LaunchedEffect(exoPlayer, editState) {
                    while (true) {
                        if (!isDragging) {
                            currentPositionMs = exoPlayer?.currentPosition ?: 0L
                            if (editState.isDoubleTrim) {
                                val ds1 = editState.doubleTrimStart1Ms.coerceIn(0L, durationMs)
                                val de1 = editState.doubleTrimEnd1Ms.coerceIn(ds1, durationMs).takeIf { it > 0 } ?: (durationMs / 2)
                                val ds2 = editState.doubleTrimStart2Ms.coerceIn(de1, durationMs)
                                val de2 = editState.doubleTrimEnd2Ms.coerceIn(ds2, durationMs).takeIf { it > 0 } ?: durationMs
                                
                                if (currentPositionMs >= de1 && currentPositionMs < ds2) {
                                    exoPlayer?.seekTo(ds2)
                                    currentPositionMs = ds2
                                } else if (currentPositionMs >= de2) {
                                    exoPlayer?.seekTo(ds1)
                                    currentPositionMs = ds1
                                } else if (currentPositionMs < ds1) {
                                    exoPlayer?.seekTo(ds1)
                                    currentPositionMs = ds1
                                }
                            } else if (!editState.isCutMode) {
                                val start = editState.trimStartMs.coerceIn(0L, durationMs)
                                val end = editState.trimEndMs.coerceIn(start, durationMs).takeIf { it > 0 } ?: durationMs
                                if (end > 0 && currentPositionMs >= end) {
                                    exoPlayer?.seekTo(start)
                                    currentPositionMs = start
                                } else if (currentPositionMs < start) {
                                    exoPlayer?.seekTo(start)
                                    currentPositionMs = start
                                }
                            } else {
                                // In cut mode, we skip the middle
                                val start = editState.trimStartMs.coerceIn(0L, durationMs)
                                val end = editState.trimEndMs.coerceIn(start, durationMs).takeIf { it > 0 } ?: durationMs
                                if (currentPositionMs >= start && currentPositionMs < end) {
                                    exoPlayer?.seekTo(end)
                                    currentPositionMs = end
                                }
                            }
                        }
                        kotlinx.coroutines.delay(50L) // Poll 20 times a second
                    }
                }"""

new_poll = """                val currentEditState by rememberUpdatedState(editState)
                LaunchedEffect(exoPlayer) {
                    while (true) {
                        if (!isDragging) {
                            currentPositionMs = exoPlayer?.currentPosition ?: 0L
                            if (currentEditState.isDoubleTrim) {
                                val ds1 = currentEditState.doubleTrimStart1Ms.coerceIn(0L, durationMs)
                                val de1 = currentEditState.doubleTrimEnd1Ms.coerceIn(ds1, durationMs).takeIf { it > 0 } ?: (durationMs / 2)
                                val ds2 = currentEditState.doubleTrimStart2Ms.coerceIn(de1, durationMs)
                                val de2 = currentEditState.doubleTrimEnd2Ms.coerceIn(ds2, durationMs).takeIf { it > 0 } ?: durationMs
                                
                                if (currentPositionMs >= de1 && currentPositionMs < ds2) {
                                    exoPlayer?.seekTo(ds2)
                                    currentPositionMs = ds2
                                } else if (currentPositionMs >= de2) {
                                    exoPlayer?.seekTo(ds1)
                                    currentPositionMs = ds1
                                } else if (currentPositionMs < ds1) {
                                    exoPlayer?.seekTo(ds1)
                                    currentPositionMs = ds1
                                }
                            } else if (!currentEditState.isCutMode) {
                                val start = currentEditState.trimStartMs.coerceIn(0L, durationMs)
                                val end = currentEditState.trimEndMs.coerceIn(start, durationMs).takeIf { it > 0 } ?: durationMs
                                if (end > 0 && currentPositionMs >= end) {
                                    exoPlayer?.seekTo(start)
                                    currentPositionMs = start
                                } else if (currentPositionMs < start) {
                                    exoPlayer?.seekTo(start)
                                    currentPositionMs = start
                                }
                            } else {
                                // In cut mode, we skip the middle
                                val start = currentEditState.trimStartMs.coerceIn(0L, durationMs)
                                val end = currentEditState.trimEndMs.coerceIn(start, durationMs).takeIf { it > 0 } ?: durationMs
                                if (currentPositionMs >= start && currentPositionMs < end) {
                                    exoPlayer?.seekTo(end)
                                    currentPositionMs = end
                                }
                            }
                        }
                        kotlinx.coroutines.delay(50L) // Poll 20 times a second
                    }
                }"""

content = content.replace(old_poll, new_poll)

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)
