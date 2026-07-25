import re

with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "r") as f:
    content = f.read()

# We need to replace the detectDragGestures part and the translationY logic.
target = """                                            detectDragGestures(
                                                onDragStart = {
                                                    draggedItemIndex = index
                                                    dragOffset = 0f
                                                },
                                                onDragEnd = {
                                                    draggedItemIndex = null
                                                    dragOffset = 0f
                                                    val newTimestamps = playlistItems.map { it.timestamp }
                                                    coroutineScope.launch {
                                                        localPlaylistItems.forEachIndexed { i, localItem ->
                                                            if (localItem.timestamp != newTimestamps[i]) {
                                                                repository.updatePlaylistItem(localItem.copy(timestamp = newTimestamps[i]))
                                                            }
                                                        }
                                                    }
                                                },
                                                onDragCancel = {
                                                    draggedItemIndex = null
                                                    dragOffset = 0f
                                                    localPlaylistItems = playlistItems
                                                }
                                            ) { change, dragAmount ->
                                                change.consume()
                                                dragOffset += dragAmount.y
                                                
                                                val threshold = itemHeightPx + spacingPx
                                                while (dragOffset > threshold && draggedItemIndex!! < localPlaylistItems.size - 1) {
                                                    val currentI = draggedItemIndex!!
                                                    val nextI = currentI + 1
                                                    val list = localPlaylistItems.toMutableList()
                                                    val temp = list[currentI]
                                                    list[currentI] = list[nextI]
                                                    list[nextI] = temp
                                                    localPlaylistItems = list
                                                    draggedItemIndex = nextI
                                                    dragOffset -= threshold
                                                }
                                                while (dragOffset < -threshold && draggedItemIndex!! > 0) {
                                                    val currentI = draggedItemIndex!!
                                                    val prevI = currentI - 1
                                                    val list = localPlaylistItems.toMutableList()
                                                    val temp = list[currentI]
                                                    list[currentI] = list[prevI]
                                                    list[prevI] = temp
                                                    localPlaylistItems = list
                                                    draggedItemIndex = prevI
                                                    dragOffset += threshold
                                                }
                                            }"""

replacement = """                                            detectDragGestures(
                                                onDragStart = {
                                                    draggedItemIndex = index
                                                    dragOffset = 0f
                                                },
                                                onDragEnd = {
                                                    if (draggedItemIndex != null) {
                                                        val threshold = itemHeightPx + spacingPx
                                                        val moveSlots = Math.round(dragOffset / threshold).toInt()
                                                            .coerceIn(-draggedItemIndex!!, localPlaylistItems.size - 1 - draggedItemIndex!!)
                                                        
                                                        if (moveSlots != 0) {
                                                            val list = localPlaylistItems.toMutableList()
                                                            val item = list.removeAt(draggedItemIndex!!)
                                                            list.add(draggedItemIndex!! + moveSlots, item)
                                                            localPlaylistItems = list
                                                            
                                                            val newTimestamps = playlistItems.map { it.timestamp }
                                                            coroutineScope.launch {
                                                                localPlaylistItems.forEachIndexed { i, localItem ->
                                                                    if (localItem.timestamp != newTimestamps[i]) {
                                                                        repository.updatePlaylistItem(localItem.copy(timestamp = newTimestamps[i]))
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                    draggedItemIndex = null
                                                    dragOffset = 0f
                                                },
                                                onDragCancel = {
                                                    draggedItemIndex = null
                                                    dragOffset = 0f
                                                }
                                            ) { change, dragAmount ->
                                                change.consume()
                                                dragOffset += dragAmount.y
                                            }"""

content = content.replace(target, replacement)

target2 = """                    val isDragging = draggedItemIndex == index
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .onSizeChanged { size ->
                                itemHeightPx = size.height.toFloat()
                            }
                            .zIndex(if (isDragging) 1f else 0f)
                            .graphicsLayer {
                                translationY = if (isDragging) dragOffset else 0f
                            }
                            .animateItem()"""

replacement2 = """                    val isDragging = draggedItemIndex == index
                    
                    val targetOffset = remember(draggedItemIndex, dragOffset, itemHeightPx, spacingPx, index, localPlaylistItems.size) {
                        if (isDragging) {
                            dragOffset
                        } else if (draggedItemIndex != null) {
                            val threshold = itemHeightPx + spacingPx
                            if (threshold > 0) {
                                val moveSlots = Math.round(dragOffset / threshold).toInt()
                                    .coerceIn(-draggedItemIndex!!, localPlaylistItems.size - 1 - draggedItemIndex!!)
                                
                                if (moveSlots > 0 && index in (draggedItemIndex!! + 1)..(draggedItemIndex!! + moveSlots)) {
                                    -threshold
                                } else if (moveSlots < 0 && index in (draggedItemIndex!! + moveSlots)..(draggedItemIndex!! - 1)) {
                                    threshold
                                } else 0f
                            } else 0f
                        } else 0f
                    }
                    
                    val animatedOffset by androidx.compose.animation.core.animateFloatAsState(
                        targetValue = targetOffset,
                        label = "offset"
                    )
                    
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .onSizeChanged { size ->
                                itemHeightPx = size.height.toFloat()
                            }
                            .zIndex(if (isDragging) 1f else 0f)
                            .graphicsLayer {
                                translationY = if (isDragging) targetOffset else animatedOffset
                            }"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "w") as f:
    f.write(content)
