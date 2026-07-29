    private fun updateCustomLayout() {
        val player = PlayerManager.exoPlayer ?: return
        val loopMode = player.repeatMode
        
        val loopIcon = when (loopMode) {
            androidx.media3.common.Player.REPEAT_MODE_ONE -> com.example.R.drawable.ic_loop_one_active
            androidx.media3.common.Player.REPEAT_MODE_ALL -> com.example.R.drawable.ic_loop_all_active
            else -> com.example.R.drawable.ic_widget_loop
        }
        val shuffleIcon = if (player.shuffleModeEnabled) com.example.R.drawable.ic_widget_shuffle_active else com.example.R.drawable.ic_widget_shuffle

        val loopAction = androidx.media3.session.CommandButton.Builder()
            .setDisplayName("Loop")
            .setSessionCommand(androidx.media3.session.SessionCommand("ACTION_LOOP", android.os.Bundle.EMPTY))
            .setIconResId(loopIcon)
            .build()
            
        val shuffleAction = androidx.media3.session.CommandButton.Builder()
            .setDisplayName("Shuffle")
            .setSessionCommand(androidx.media3.session.SessionCommand("ACTION_SHUFFLE", android.os.Bundle.EMPTY))
            .setIconResId(shuffleIcon)
            .build()
            
        val pipAction = androidx.media3.session.CommandButton.Builder()
            .setDisplayName("PiP")
            .setSessionCommand(androidx.media3.session.SessionCommand("ACTION_PIP", android.os.Bundle.EMPTY))
            .setIconResId(com.example.R.drawable.ic_pip)
            .build()

        mediaSession?.setCustomLayout(listOf(loopAction, shuffleAction, pipAction))
    }

    override fun onDestroy() {
        if (::widgetCommandReceiver.isInitialized) {
            unregisterReceiver(widgetCommandReceiver)
        }
        mediaSession?.run {
            player.release()
            release()
            mediaSession = null
        }
        lifecycleRegistry.handleLifecycleEvent(androidx.lifecycle.Lifecycle.Event.ON_DESTROY)
        hideOverlay()
        super.onDestroy()
    }

    private fun updateWidgetUI() {
        val appWidgetManager = android.appwidget.AppWidgetManager.getInstance(this)
        val componentName = android.content.ComponentName(this, com.example.widget.MediaWidgetProvider::class.java)
        val appWidgetIds = appWidgetManager.getAppWidgetIds(componentName)
        if (appWidgetIds.isNotEmpty()) {
            val player = PlayerManager.exoPlayer ?: return
            for (appWidgetId in appWidgetIds) {
                val views = android.widget.RemoteViews(packageName, com.example.R.layout.widget_media)
                views.setTextViewText(com.example.R.id.widget_title, player.currentMediaItem?.mediaMetadata?.title?.toString() ?: "No Media")
                views.setImageViewResource(com.example.R.id.widget_btn_play, if (player.isPlaying) com.example.R.drawable.ic_widget_pause else com.example.R.drawable.ic_widget_play)
                
                val duration = player.duration.coerceAtLeast(0)
                val position = player.currentPosition.coerceAtLeast(0)
                views.setProgressBar(com.example.R.id.widget_progress, duration.toInt(), position.toInt(), false)

                appWidgetManager.updateAppWidget(appWidgetId, views)
                appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetId, com.example.R.id.widget_list)
            }
        }
    }

    private val widgetCommandReceiver = object : android.content.BroadcastReceiver() {
        override fun onReceive(context: android.content.Context, intent: android.content.Intent) {
            if (intent.action == "com.example.ACTION_UPDATE_NOTIFICATION") {
                updateCustomLayout()
                return
            }
            val player = PlayerManager.exoPlayer ?: return
            when (intent.getStringExtra("command")) {
                "ACTION_MINIPLAYER", "ACTION_OVERLAY" -> showOverlay()
                "ACTION_CLOSE" -> {
                    player.stop()
                    player.clearMediaItems()
                    hideOverlay()
                    stopSelf()
                }
                "ACTION_PLAY_PAUSE" -> if (player.isPlaying) player.pause() else player.play()
                "ACTION_PREV" -> player.seekToPreviousMediaItem()
                "ACTION_NEXT" -> player.seekToNextMediaItem()
                "ACTION_PLAY_ITEM" -> {
                    val index = intent.getIntExtra("index", -1)
                    if (index >= 0) player.seekToDefaultPosition(index)
                }
                "ACTION_PLAY_FILE" -> {
                    val uriStr = intent.getStringExtra("uri")
                    if (uriStr != null) {
                        val mediaItem = androidx.media3.common.MediaItem.Builder()
                            .setUri(uriStr)
                            .setMediaId(uriStr)
                            .setMediaMetadata(
                                androidx.media3.common.MediaMetadata.Builder()
                                    .setTitle(android.net.Uri.parse(uriStr).lastPathSegment ?: "Unknown")
                                    .build()
                            )
                            .build()
                        player.setMediaItem(mediaItem)
                        player.prepare()
                        player.play()
                    }
                }
            }
            updateWidgetUI()
        }
    }
}
