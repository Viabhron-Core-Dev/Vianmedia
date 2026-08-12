import re

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

loop_old = re.search(r'LaunchedEffect\(exoPlayer\) \{.*?kotlinx\.coroutines\.delay\(50L\) // Poll 20 times a second\n                    \}\n                \}', content, re.DOTALL).group(0)

loop_new = """val mainVideoIndex = if (currentEditState.joinVideoUri != null && !currentEditState.joinAtEnd) 1 else 0
                val totalItems = if (currentEditState.joinVideoUri != null) 2 else 1
                LaunchedEffect(exoPlayer) {
                    while (true) {
                        if (!isDragging) {
                            val currentIndex = exoPlayer?.currentMediaItemIndex ?: 0
                            currentPositionMs = exoPlayer?.currentPosition ?: 0L
                            
                            if (currentIndex == mainVideoIndex) {
                                if (currentEditState.isDoubleTrim) {
                                    val ds1 = currentEditState.doubleTrimStart1Ms.coerceIn(0L, durationMs)
                                    val de1 = currentEditState.doubleTrimEnd1Ms.coerceIn(ds1, durationMs).takeIf { it > 0 } ?: (durationMs / 2)
                                    val ds2 = currentEditState.doubleTrimStart2Ms.coerceIn(de1, durationMs)
                                    val de2 = currentEditState.doubleTrimEnd2Ms.coerceIn(ds2, durationMs).takeIf { it > 0 } ?: durationMs
                                    
                                    if (currentPositionMs >= de1 && currentPositionMs < ds2) {
                                        exoPlayer?.seekTo(mainVideoIndex, ds2)
                                        currentPositionMs = ds2
                                    } else if (currentPositionMs >= de2) {
                                        val nextIndex = (mainVideoIndex + 1) % totalItems
                                        val nextPos = if (nextIndex == mainVideoIndex) ds1 else 0L
                                        exoPlayer?.seekTo(nextIndex, nextPos)
                                        currentPositionMs = nextPos
                                    } else if (currentPositionMs < ds1) {
                                        exoPlayer?.seekTo(mainVideoIndex, ds1)
                                        currentPositionMs = ds1
                                    }
                                } else if (!currentEditState.isCutMode) {
                                    val start = currentEditState.trimStartMs.coerceIn(0L, durationMs)
                                    val end = currentEditState.trimEndMs.coerceIn(start, durationMs).takeIf { it > 0 } ?: durationMs
                                    if (end > 0 && currentPositionMs >= end) {
                                        val nextIndex = (mainVideoIndex + 1) % totalItems
                                        val nextPos = if (nextIndex == mainVideoIndex) start else 0L
                                        exoPlayer?.seekTo(nextIndex, nextPos)
                                        currentPositionMs = nextPos
                                    } else if (currentPositionMs < start) {
                                        exoPlayer?.seekTo(mainVideoIndex, start)
                                        currentPositionMs = start
                                    }
                                } else {
                                    // In cut mode, we skip the middle
                                    val start = currentEditState.trimStartMs.coerceIn(0L, durationMs)
                                    val end = currentEditState.trimEndMs.coerceIn(start, durationMs).takeIf { it > 0 } ?: durationMs
                                    if (currentPositionMs >= start && currentPositionMs < end) {
                                        exoPlayer?.seekTo(mainVideoIndex, end)
                                        currentPositionMs = end
                                    }
                                    if (currentPositionMs >= durationMs) {
                                        val nextIndex = (mainVideoIndex + 1) % totalItems
                                        val nextPos = if (nextIndex == mainVideoIndex) 0L else 0L
                                        exoPlayer?.seekTo(nextIndex, nextPos)
                                        currentPositionMs = nextPos
                                    }
                                }
                            }
                        }
                        kotlinx.coroutines.delay(50L) // Poll 20 times a second
                    }
                }"""

content = content.replace(loop_old, loop_new)

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
