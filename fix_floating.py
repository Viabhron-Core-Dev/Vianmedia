with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

target = """    if (isMinimizedExternal) {
        Box(
            modifier = Modifier
                .size(40.dp)
                .clip(androidx.compose.foundation.shape.CircleShape)
                .background(MaterialTheme.colorScheme.surface)
                .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.3f), androidx.compose.foundation.shape.CircleShape)
                .pointerInput(Unit) {
                    detectDragGesturesAfterLongPress(
                        onDrag = { change: androidx.compose.ui.input.pointer.PointerInputChange, dragAmount: androidx.compose.ui.geometry.Offset ->
                            change.consume()
                            onDrag(dragAmount.x, dragAmount.y)
                        }
                    )
                }
                .clickable { onMinimizeChange(false) },
            contentAlignment = Alignment.Center
        ) {
            Icon(androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_play_launcher_foreground), contentDescription = "Unfold", tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(20.dp))
        }
        return
    }"""

replacement = """    if (isMinimizedExternal) {
        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(androidx.compose.foundation.shape.CircleShape)
                .background(androidx.compose.ui.graphics.Color(0xFF2196F3))
                .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.3f), androidx.compose.foundation.shape.CircleShape)
                .pointerInput(Unit) {
                    detectDragGesturesAfterLongPress(
                        onDrag = { change: androidx.compose.ui.input.pointer.PointerInputChange, dragAmount: androidx.compose.ui.geometry.Offset ->
                            change.consume()
                            onDrag(dragAmount.x, dragAmount.y)
                        }
                    )
                }
                .clickable { onMinimizeChange(false) },
            contentAlignment = Alignment.Center
        ) {
            androidx.compose.foundation.Image(
                painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_launcher_foreground),
                contentDescription = "Unfold",
                modifier = Modifier.fillMaxSize()
            )
        }
        return
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
