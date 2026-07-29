with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

target = """                Slider(
                    value = if (durationMs > 0) (currentPositionMs.toFloat() / durationMs.toFloat()).coerceIn(0f, 1f) else 0f,
                    onValueChange = { 
                        isDragging = true
                        currentPositionMs = (it * durationMs).toLong()
                        exoPlayer?.seekTo(currentPositionMs)
                    },
                    onValueChangeFinished = {
                        isDragging = false
                    },
                    modifier = Modifier.fillMaxWidth()
                )"""

replacement = """                @OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
                Slider(
                    value = if (durationMs > 0) (currentPositionMs.toFloat() / durationMs.toFloat()).coerceIn(0f, 1f) else 0f,
                    onValueChange = { 
                        isDragging = true
                        currentPositionMs = (it * durationMs).toLong()
                        exoPlayer?.seekTo(currentPositionMs)
                    },
                    onValueChangeFinished = {
                        isDragging = false
                    },
                    modifier = Modifier.fillMaxWidth(),
                    track = { sliderState ->
                        val isTrimMode = currentTool == VideoEditorTool.TRIM
                        val startFraction = if (isTrimMode && editState.trimStartMs > 0) editState.trimStartMs.toFloat() / durationMs.toFloat() else 0f
                        val endFraction = if (isTrimMode && editState.trimEndMs > 0) editState.trimEndMs.toFloat() / durationMs.toFloat() else 1f
                        
                        androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxWidth().height(4.dp)) {
                            val startX = startFraction * size.width
                            val endX = endFraction * size.width
                            
                            if (isTrimMode) {
                                // Inactive track only within cut
                                drawLine(
                                    color = Color.Gray.copy(alpha = 0.5f),
                                    start = androidx.compose.ui.geometry.Offset(startX, size.height / 2),
                                    end = androidx.compose.ui.geometry.Offset(endX, size.height / 2),
                                    strokeWidth = 4.dp.toPx(),
                                    cap = androidx.compose.ui.graphics.StrokeCap.Round
                                )
                                
                                val currentX = (sliderState.value * size.width).coerceIn(startX, endX)
                                if (currentX > startX) {
                                    drawLine(
                                        color = Color(0xFF2196F3),
                                        start = androidx.compose.ui.geometry.Offset(startX, size.height / 2),
                                        end = androidx.compose.ui.geometry.Offset(currentX, size.height / 2),
                                        strokeWidth = 4.dp.toPx(),
                                        cap = androidx.compose.ui.graphics.StrokeCap.Round
                                    )
                                }
                            } else {
                                // Default track
                                drawLine(
                                    color = Color.Gray.copy(alpha = 0.5f),
                                    start = androidx.compose.ui.geometry.Offset(0f, size.height / 2),
                                    end = androidx.compose.ui.geometry.Offset(size.width, size.height / 2),
                                    strokeWidth = 4.dp.toPx(),
                                    cap = androidx.compose.ui.graphics.StrokeCap.Round
                                )
                                drawLine(
                                    color = Color(0xFF2196F3),
                                    start = androidx.compose.ui.geometry.Offset(0f, size.height / 2),
                                    end = androidx.compose.ui.geometry.Offset(sliderState.value * size.width, size.height / 2),
                                    strokeWidth = 4.dp.toPx(),
                                    cap = androidx.compose.ui.graphics.StrokeCap.Round
                                )
                            }
                        }
                    }
                )"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Replaced Slider successfully.")
else:
    print("Target Slider not found.")
