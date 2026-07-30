with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

target = """                                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                        Text(formatMs(start.toLong()), style = MaterialTheme.typography.labelMedium)
                                        
                                        var customCutText by remember { mutableStateOf("") }
                                        androidx.compose.foundation.text.BasicTextField(
                                            value = if (customCutText.isEmpty()) "Cut: ${formatMs((end - start).toLong())}" else customCutText,
                                            onValueChange = { customCutText = it },
                                            textStyle = MaterialTheme.typography.labelMedium.copy(
                                                color = MaterialTheme.colorScheme.primary,
                                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                                            ),
                                            modifier = Modifier.weight(1f).padding(horizontal = 8.dp)
                                        )
                                        
                                        Text(formatMs(end.toLong()), style = MaterialTheme.typography.labelMedium)
                                    }
                                    RangeSlider(
                                        value = start..end,
                                        onValueChange = { range ->
                                            val oldStart = editState.trimStartMs
                                            editState = editState.copy(
                                                trimStartMs = range.start.toLong(),
                                                trimEndMs = range.endInclusive.toLong()
                                            )
                                            if (Math.abs(range.start.toLong() - oldStart) > 100) {
                                                exoPlayer?.seekTo(range.start.toLong())
                                            } else {
                                                exoPlayer?.seekTo(range.endInclusive.toLong())
                                            }
                                        },
                                        valueRange = 0f..durationMs.toFloat().coerceAtLeast(1f),
                                        modifier = Modifier.fillMaxWidth()
                                    )"""

replacement = """                                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                        var startText by remember(start) { mutableStateOf(formatMs(start.toLong())) }
                                        androidx.compose.foundation.text.BasicTextField(
                                            value = startText,
                                            onValueChange = { 
                                                startText = it
                                                val parts = it.split(":")
                                                var ms = -1L
                                                if (parts.size == 2) {
                                                    ms = ((parts[0].toLongOrNull() ?: 0L) * 60 + (parts[1].toLongOrNull() ?: 0L)) * 1000
                                                } else if (parts.size == 1) {
                                                    val parsed = parts[0].toLongOrNull()
                                                    if (parsed != null) ms = parsed * 1000
                                                }
                                                if (ms >= 0) {
                                                    editState = editState.copy(trimStartMs = ms.coerceIn(0L, end.toLong()))
                                                    exoPlayer?.seekTo(ms.coerceIn(0L, end.toLong()))
                                                }
                                            },
                                            textStyle = MaterialTheme.typography.labelMedium.copy(color = MaterialTheme.colorScheme.onSurface, textAlign = androidx.compose.ui.text.style.TextAlign.Center),
                                            keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number),
                                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), RoundedCornerShape(4.dp)).padding(4.dp).widthIn(min = 40.dp)
                                        )
                                        
                                        var customCutText by remember { mutableStateOf("") }
                                        androidx.compose.foundation.text.BasicTextField(
                                            value = if (customCutText.isEmpty()) "Cut: ${formatMs((end - start).toLong())}" else customCutText,
                                            onValueChange = { customCutText = it },
                                            textStyle = MaterialTheme.typography.labelMedium.copy(
                                                color = MaterialTheme.colorScheme.primary,
                                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                                            ),
                                            modifier = Modifier.weight(1f).padding(horizontal = 8.dp)
                                        )
                                        
                                        var endText by remember(end) { mutableStateOf(formatMs(end.toLong())) }
                                        androidx.compose.foundation.text.BasicTextField(
                                            value = endText,
                                            onValueChange = { 
                                                endText = it
                                                val parts = it.split(":")
                                                var ms = -1L
                                                if (parts.size == 2) {
                                                    ms = ((parts[0].toLongOrNull() ?: 0L) * 60 + (parts[1].toLongOrNull() ?: 0L)) * 1000
                                                } else if (parts.size == 1) {
                                                    val parsed = parts[0].toLongOrNull()
                                                    if (parsed != null) ms = parsed * 1000
                                                }
                                                if (ms >= 0) {
                                                    editState = editState.copy(trimEndMs = ms.coerceIn(start.toLong(), durationMs))
                                                    exoPlayer?.seekTo(ms.coerceIn(start.toLong(), durationMs))
                                                }
                                            },
                                            textStyle = MaterialTheme.typography.labelMedium.copy(color = MaterialTheme.colorScheme.onSurface, textAlign = androidx.compose.ui.text.style.TextAlign.Center),
                                            keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number),
                                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), RoundedCornerShape(4.dp)).padding(4.dp).widthIn(min = 40.dp)
                                        )
                                    }
                                    
                                    val activeTrackColor = if (editState.isCutMode) MaterialTheme.colorScheme.surfaceVariant else MaterialTheme.colorScheme.primary
                                    val inactiveTrackColor = if (editState.isCutMode) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
                                    
                                    RangeSlider(
                                        value = start..end,
                                        onValueChange = { range ->
                                            val oldStart = editState.trimStartMs
                                            editState = editState.copy(
                                                trimStartMs = range.start.toLong(),
                                                trimEndMs = range.endInclusive.toLong()
                                            )
                                            if (Math.abs(range.start.toLong() - oldStart) > 100) {
                                                exoPlayer?.seekTo(range.start.toLong())
                                            } else {
                                                exoPlayer?.seekTo(range.endInclusive.toLong())
                                            }
                                        },
                                        valueRange = 0f..durationMs.toFloat().coerceAtLeast(1f),
                                        modifier = Modifier.fillMaxWidth(),
                                        colors = androidx.compose.material3.SliderDefaults.colors(
                                            activeTrackColor = activeTrackColor,
                                            inactiveTrackColor = inactiveTrackColor
                                        )
                                    )"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
