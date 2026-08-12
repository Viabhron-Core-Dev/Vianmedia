import re

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

# Add currentIndex state
state_replace = """var currentPositionMs by remember { mutableLongStateOf(0L) }
                var currentIndex by remember { mutableIntStateOf(0) }"""
content = content.replace('var currentPositionMs by remember { mutableLongStateOf(0L) }', state_replace)

# Update currentIndex in loop
loop_idx = """val currentIndexRaw = exoPlayer?.currentMediaItemIndex ?: 0
                            currentIndex = currentIndexRaw
                            currentPositionMs = exoPlayer?.currentPosition ?: 0L"""
content = content.replace('val currentIndex = exoPlayer?.currentMediaItemIndex ?: 0\n                            currentPositionMs = exoPlayer?.currentPosition ?: 0L', loop_idx)
content = content.replace('currentIndex == mainVideoIndex', 'currentIndexRaw == mainVideoIndex')

# Now update timeline calculation
old_timeline = re.search(r'var virtualDurationMs = durationMs\n                var virtualPositionMs = currentPositionMs\n                   \n                if \(true\) \{ // Always show virtual timeline\n                    if \(editState\.isDoubleTrim\) \{.*?\} else \{.*?\n                        \}\n                    \}\n                \}', content, re.DOTALL).group(0)

new_timeline = """var virtualDurationMs = durationMs
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
                
                // Add join video duration
                if (editState.joinVideoUri != null) {
                    val mainDur = virtualDurationMs
                    virtualDurationMs += joinDurationMs
                    
                    if (currentIndex == mainVideoIndex) {
                        if (!editState.joinAtEnd) {
                            virtualPositionMs += joinDurationMs
                        }
                    } else {
                        // We are in join video
                        virtualPositionMs = currentPositionMs
                        if (editState.joinAtEnd) {
                            virtualPositionMs += mainDur
                        }
                    }
                }
"""
content = content.replace(old_timeline, new_timeline)

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
