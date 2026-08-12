import re

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

# Add a state for join video duration
duration_state = """var durationMs by remember { mutableLongStateOf(1L) }
    var joinDurationMs by remember { mutableLongStateOf(0L) }"""

content = content.replace('var durationMs by remember { mutableLongStateOf(1L) }', duration_state)

# Add retriever for join video
retriever_join = """    LaunchedEffect(editState.joinVideoUri) {
        if (editState.joinVideoUri != null) {
            try {
                val retriever = android.media.MediaMetadataRetriever()
                retriever.setDataSource(context, android.net.Uri.parse(editState.joinVideoUri))
                val timeString = retriever.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_DURATION)
                if (timeString != null) {
                    joinDurationMs = timeString.toLong()
                }
                retriever.release()
            } catch (e: Exception) {}
        } else {
            joinDurationMs = 0L
        }
    }"""

content = content.replace('val effectiveMimeType = if (convertedUri != null) "video/mp4" else mimeType', 'val effectiveMimeType = if (convertedUri != null) "video/mp4" else mimeType\n' + retriever_join)

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
