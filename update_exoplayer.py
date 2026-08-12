import re

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

# 1. Add LaunchedEffect for durationMs just before `val exoPlayer = remember...`
duration_effect = """
    LaunchedEffect(effectiveUri) {
        try {
            val retriever = android.media.MediaMetadataRetriever()
            retriever.setDataSource(context, android.net.Uri.parse(effectiveUri.toString()))
            val timeString = retriever.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_DURATION)
            if (timeString != null) {
                val dur = timeString.toLong()
                if (dur > 0) {
                    durationMs = dur
                    if (editState.trimEndMs == 0L) {
                        editState = editState.copy(trimEndMs = dur)
                    }
                }
            }
            retriever.release()
        } catch (e: Exception) {}
    }
"""

# 2. Replace exoPlayer remember block
old_exoplayer_block = re.search(r'val exoPlayer = remember\(effectiveUri\) \{.*?(?=    if \(exoPlayer != null\))', content, re.DOTALL).group(0)

new_exoplayer_block = """val exoPlayer = remember(effectiveUri, editState.joinVideoUri, editState.joinAtEnd) {
        val uriToUse = if (mimeType == "image/gif" || mimeType == "image/webp") convertedUri else effectiveUri?.toString()
        if (uriToUse == null) null
        else androidx.media3.exoplayer.ExoPlayer.Builder(context).build().apply {
            val items = mutableListOf<androidx.media3.common.MediaItem>()
            val mainItem = androidx.media3.common.MediaItem.fromUri(android.net.Uri.parse(uriToUse))
            val joinItem = editState.joinVideoUri?.let { androidx.media3.common.MediaItem.fromUri(android.net.Uri.parse(it)) }
            
            if (joinItem != null && !editState.joinAtEnd) {
                items.add(joinItem)
            }
            items.add(mainItem)
            if (joinItem != null && editState.joinAtEnd) {
                items.add(joinItem)
            }
            
            setMediaItems(items)
            repeatMode = androidx.media3.common.Player.REPEAT_MODE_ALL
            prepare()
            playWhenReady = true
            addListener(object : androidx.media3.common.Player.Listener {
                override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
                    if (videoSize.width > 0 && videoSize.height > 0 && videoWidth <= 1) {
                        @Suppress("DEPRECATION")
                        if (videoSize.unappliedRotationDegrees == 90 || videoSize.unappliedRotationDegrees == 270) {
                            videoWidth = videoSize.height
                            videoHeight = videoSize.width
                        } else {
                            videoWidth = videoSize.width
                            videoHeight = videoSize.height
                        }
                    }
                }
            })
        }
    }
"""

content = content.replace(old_exoplayer_block, duration_effect + "\n    " + new_exoplayer_block)

# 3. Modify onPlaybackStateChanged duration fetch
old_duration_fetch = """val dur = exoPlayer.duration
                        if (dur > 0) {
                            durationMs = dur
                            if (editState.trimEndMs == 0L) {
                                editState = editState.copy(trimEndMs = dur)
                            }
                            LogKeeper.log("ExoPlayer is READY. Loaded video duration: ${formatMs(dur)}", "VideoEditor")
                        }"""
                        
new_duration_fetch = """// Duration is now fetched via MediaMetadataRetriever to avoid playlist issues
                        LogKeeper.log("ExoPlayer is READY.", "VideoEditor")"""

content = content.replace(old_duration_fetch, new_duration_fetch)

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
