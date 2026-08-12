LaunchedEffect(effectiveUri) {
    try {
        val retriever = android.media.MediaMetadataRetriever()
        retriever.setDataSource(context, android.net.Uri.parse(effectiveUri))
        val timeString = retriever.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_DURATION)
        if (timeString != null) {
            val d = timeString.toLong()
            if (d > 0) durationMs = d
        }
        retriever.release()
    } catch (e: Exception) {}
}
