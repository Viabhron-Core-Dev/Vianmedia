import re

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

# I will replace the entire onReceive method from `override fun onReceive(context: Context, intent: Intent) {` to the end of the class.

start_idx = content.find("override fun onReceive(context: Context, intent: Intent) {")
if start_idx != -1:
    new_content = content[:start_idx] + """override fun onReceive(context: Context, intent: Intent) {
        val action = intent.action
        com.example.LogKeeper.log("onReceive action: $action", "MediaWidgetProvider")
        
        if (action == "ACTION_REFRESH" || action == "android.appwidget.action.APPWIDGET_UPDATE" || action == "android.appwidget.action.APPWIDGET_UPDATE_OPTIONS" || action == "android.appwidget.action.APPWIDGET_ENABLED" || action == "android.appwidget.action.APPWIDGET_DISABLED" || action == "android.appwidget.action.APPWIDGET_DELETED") {
            try {
                super.onReceive(context, intent)
                if (action == "ACTION_REFRESH") {
                    updateWidgets(context)
                }
            } catch (e: Exception) {
                com.example.LogKeeper.logError("MediaWidgetProvider", "Error in onReceive standard action", e)
            }
            return
        }
        
        if (action == "ACTION_REWIND") {
            val player = com.example.service.PlayerManager.exoPlayer
            player?.seekTo((player.currentPosition - 5000).coerceAtLeast(0))
            return
        }
        if (action == "ACTION_FFWD") {
            val player = com.example.service.PlayerManager.exoPlayer
            player?.seekTo((player.currentPosition + 5000).coerceAtMost(player.duration ?: 0))
            return
        }
        if (action == "ACTION_STOP") {
            val player = com.example.service.PlayerManager.exoPlayer
            player?.stop()
            player?.clearMediaItems()
            updateWidgets(context)
            return
        }
        
        if (action == "ACTION_BACK_FOLDER") {
            val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
            val currentMode = prefs.getString("explorer_mode", "current") ?: "current"
            val searchQuery = prefs.getString("search_query", "")
            
            if (searchQuery?.isNotBlank() == true) {
                prefs.edit().putString("search_query", "").apply()
            } else if (currentMode == "folder_items") {
                prefs.edit().putString("explorer_mode", "folders").putString("folder_id", null).apply()
            } else if (currentMode == "folders" || currentMode == "current" || currentMode == "playlists") {
                prefs.edit().putString("explorer_mode", "root").apply()
            }
            
            updateWidgets(context)
            return
        }

        if (action == "ACTION_PLAY_ITEM") {
            val widgetAction = intent.getStringExtra("WIDGET_ACTION")
            val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
            
            when (widgetAction) {
                "NAVIGATE_CURRENT" -> {
                    prefs.edit().putString("explorer_mode", "current").apply()
                    updateWidgets(context)
                    return
                }
                "NAVIGATE_FOLDERS" -> {
                    prefs.edit().putString("explorer_mode", "folders").putString("folder_id", null).apply()
                    updateWidgets(context)
                    return
                }
                "NAVIGATE_PLAYLISTS" -> {
                    prefs.edit().putString("explorer_mode", "playlists").apply()
                    updateWidgets(context)
                    return
                }
                "OPEN_FOLDER" -> {
                    val folderId = intent.getStringExtra("FOLDER_ID")
                    prefs.edit().putString("explorer_mode", "folder_items").putString("folder_id", folderId).apply()
                    updateWidgets(context)
                    return
                }
            }
        }

        // Media controller commands
        val widgetAction = intent.getStringExtra("WIDGET_ACTION")
        val isMediaCommand = action in listOf("ACTION_PLAY_PAUSE", "ACTION_PREV", "ACTION_NEXT", "ACTION_LOOP", "ACTION_SHUFFLE", "ACTION_MINIPLAYER", "ACTION_CLOSE") || 
                             (action == "ACTION_PLAY_ITEM" && (widgetAction == "PLAY_FILE" || widgetAction == "PLAYLIST_ITEM" || widgetAction == null))

        if (isMediaCommand) {
            val pendingResult = goAsync()
            val sessionToken = androidx.media3.session.SessionToken(context, android.content.ComponentName(context, com.example.service.PlaybackService::class.java))
            val controllerFuture = androidx.media3.session.MediaController.Builder(context, sessionToken).buildAsync()
            
            controllerFuture.addListener({
                try {
                    val controller = controllerFuture.get()
                    if (action == "ACTION_PLAY_PAUSE") {
                        if (controller.isPlaying) controller.pause() else controller.play()
                    } else if (action == "ACTION_PREV") {
                        controller.seekToPreviousMediaItem()
                    } else if (action == "ACTION_NEXT") {
                        controller.seekToNextMediaItem()
                    } else if (action == "ACTION_LOOP") {
                        val nextMode = when (controller.repeatMode) {
                            androidx.media3.common.Player.REPEAT_MODE_OFF -> androidx.media3.common.Player.REPEAT_MODE_ALL
                            androidx.media3.common.Player.REPEAT_MODE_ALL -> androidx.media3.common.Player.REPEAT_MODE_ONE
                            else -> androidx.media3.common.Player.REPEAT_MODE_OFF
                        }
                        controller.repeatMode = nextMode
                    } else if (action == "ACTION_SHUFFLE") {
                        controller.shuffleModeEnabled = !controller.shuffleModeEnabled
                    } else if (action == "ACTION_CLOSE") {
                        controller.stop()
                        controller.clearMediaItems()
                        // send broadcast to close service
                        val serviceIntent = Intent("com.example.ACTION_WIDGET_COMMAND")
                        serviceIntent.setPackage(context.packageName)
                        serviceIntent.putExtra("command", action)
                        context.sendBroadcast(serviceIntent)
                    } else if (action == "ACTION_MINIPLAYER") {
                        val serviceIntent = Intent("com.example.ACTION_WIDGET_COMMAND")
                        serviceIntent.setPackage(context.packageName)
                        serviceIntent.putExtra("command", action)
                        context.sendBroadcast(serviceIntent)
                    } else if (action == "ACTION_PLAY_ITEM") {
                        if (widgetAction == "PLAY_FILE") {
                            val uriStr = intent.getStringExtra("MEDIA_URI")
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
                                controller.setMediaItem(mediaItem)
                                controller.prepare()
                                controller.play()
                            }
                        } else {
                            val index = intent.getIntExtra("EXTRA_INDEX", -1)
                            if (index >= 0) controller.seekToDefaultPosition(index)
                        }
                    }
                    
                    updateWidgets(context)
                    
                    androidx.media3.session.MediaController.releaseFuture(controllerFuture)
                } catch (e: Exception) {
                    com.example.LogKeeper.logError("MediaWidgetProvider", "Error in MediaController logic", e)
                } finally {
                    pendingResult.finish()
                }
            }, androidx.core.content.ContextCompat.getMainExecutor(context))
        }
    }
}
"""
    with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
        f.write(new_content)
    print("Replaced onReceive")
else:
    print("Failed to replace onReceive")
