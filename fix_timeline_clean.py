import re

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

# Fix duplicate mainVideoIndex
content = content.replace('val mainVideoIndex = if (currentEditState.joinVideoUri != null && !currentEditState.joinAtEnd) 1 else 0', 'val mainVideoIndexState = if (currentEditState.joinVideoUri != null && !currentEditState.joinAtEnd) 1 else 0')
content = content.replace('currentIndexRaw == mainVideoIndex', 'currentIndexRaw == mainVideoIndexState')
content = content.replace('seekTo(mainVideoIndex', 'seekTo(mainVideoIndexState')
content = content.replace('nextIndex == mainVideoIndex', 'nextIndex == mainVideoIndexState')

pattern = re.compile(r'val isTrimMode = currentTool == VideoEditorTool\.TRIM(.*?)Slider\(', re.DOTALL)

new_block = """val isTrimMode = currentTool == VideoEditorTool.TRIM
                
                var virtualDurationMs = durationMs
                var virtualPositionMs = currentPositionMs
                val mainVideoIndex = if (editState.joinVideoUri != null && !editState.joinAtEnd) 1 else 0
                
                if (true) { 
                    if (editState.isDoubleTrim) {
                        val ds1 = editState.doubleTrimStart1Ms.coerceIn(0L, durationMs)
                        val de1 = editState.doubleTrimEnd1Ms.coerceIn(ds1, durationMs).takeIf { it > 0 } ?: (durationMs / 2)
                        val ds2 = editState.doubleTrimStart2Ms.coerceIn(de1, durationMs)
                        val de2 = editState.doubleTrimEnd2Ms.coerceIn(ds2, durationMs).takeIf { it > 0 } ?: durationMs
                           
                        val dur1 = (de1 - ds1).coerceAtLeast(0)
                        val dur2 = (de2 - ds2).coerceAtLeast(0)
                        virtualDurationMs = dur1 + dur2
                           
                        virtualPositionMs = when {
                            currentPositionMs < ds1 -> 0L
                            currentPositionMs <= de1 -> currentPositionMs - ds1
                            currentPositionMs < ds2 -> dur1
                            currentPositionMs <= de2 -> dur1 + (currentPositionMs - ds2)
                            else -> dur1 + dur2
                        }
                    } else if (editState.isCutMode) {
                        val start = editState.trimStartMs.coerceIn(0L, durationMs)
                        val end = editState.trimEndMs.coerceIn(start, durationMs).takeIf { it > 0 } ?: durationMs
                           
                        val dur1 = start
                        val dur2 = (durationMs - end).coerceAtLeast(0)
                        virtualDurationMs = dur1 + dur2
                           
                        virtualPositionMs = when {
                            currentPositionMs <= start -> currentPositionMs
                            currentPositionMs < end -> dur1
                            else -> dur1 + (currentPositionMs - end)
                        }
                    } else {
                        val start = editState.trimStartMs.coerceIn(0L, durationMs)
                        val end = editState.trimEndMs.coerceIn(start, durationMs).takeIf { it > 0 } ?: durationMs
                           
                        virtualDurationMs = (end - start).coerceAtLeast(0)
                           
                        virtualPositionMs = when {
                            currentPositionMs < start -> 0L
                            currentPositionMs <= end -> currentPositionMs - start
                            else -> virtualDurationMs
                        }
                    }
                }
                
                if (editState.joinVideoUri != null) {
                    val mainDur = virtualDurationMs
                    virtualDurationMs += joinDurationMs
                    
                    if (currentIndex == mainVideoIndex) {
                        if (!editState.joinAtEnd) {
                            virtualPositionMs += joinDurationMs
                        }
                    } else {
                        virtualPositionMs = currentPositionMs
                        if (editState.joinAtEnd) {
                            virtualPositionMs += mainDur
                        }
                    }
                }
                   
                Slider("""

content = pattern.sub(new_block, content)

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
