import re

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

pattern = re.compile(r'onValueChange = \{ value ->.*?exoPlayer\?\.seekTo\(currentPositionMs\)\s*\},', re.DOTALL)

new_slider = """onValueChange = { value ->
                        isDragging = true
                        val newVirtualPos = (value * virtualDurationMs).toLong()
                        
                        val mainVideoIndexState = if (editState.joinVideoUri != null && !editState.joinAtEnd) 1 else 0
                        val mainDur = if (editState.joinVideoUri != null) virtualDurationMs - joinDurationMs else virtualDurationMs
                        
                        val isJoinPlay = if (editState.joinVideoUri != null) {
                            if (editState.joinAtEnd) newVirtualPos > mainDur else newVirtualPos < joinDurationMs
                        } else false
                        
                        if (isJoinPlay) {
                            val targetIndex = if (editState.joinAtEnd) 1 else 0
                            val targetPos = if (editState.joinAtEnd) newVirtualPos - mainDur else newVirtualPos
                            currentPositionMs = targetPos
                            currentIndex = targetIndex
                            exoPlayer?.seekTo(targetIndex, targetPos)
                        } else {
                            val mainVirtualPos = if (editState.joinVideoUri != null && !editState.joinAtEnd) newVirtualPos - joinDurationMs else newVirtualPos
                            var newRealPos = mainVirtualPos
                            
                            if (true) {
                                if (editState.isDoubleTrim) {
                                    val ds1 = editState.doubleTrimStart1Ms.coerceIn(0L, durationMs)
                                    val de1 = editState.doubleTrimEnd1Ms.coerceIn(ds1, durationMs).takeIf { it > 0 } ?: (durationMs / 2)
                                    val ds2 = editState.doubleTrimStart2Ms.coerceIn(de1, durationMs)
                                    val dur1 = (de1 - ds1).coerceAtLeast(0)
                                       
                                    newRealPos = if (mainVirtualPos <= dur1) {
                                        ds1 + mainVirtualPos
                                    } else {
                                        ds2 + (mainVirtualPos - dur1)
                                    }
                                } else if (editState.isCutMode) {
                                    val start = editState.trimStartMs.coerceIn(0L, durationMs)
                                    val end = editState.trimEndMs.coerceIn(start, durationMs).takeIf { it > 0 } ?: durationMs
                                       
                                    newRealPos = if (mainVirtualPos <= start) {
                                        mainVirtualPos
                                    } else {
                                        end + (mainVirtualPos - start)
                                    }
                                } else {
                                    val start = editState.trimStartMs.coerceIn(0L, durationMs)
                                    newRealPos = start + mainVirtualPos
                                }
                            }
                               
                            currentPositionMs = newRealPos.coerceIn(0, durationMs)
                            currentIndex = mainVideoIndexState
                            exoPlayer?.seekTo(mainVideoIndexState, currentPositionMs)
                        }
                    },"""

content = pattern.sub(new_slider, content)

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
