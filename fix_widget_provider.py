with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

target = """    override fun onReceive(context: Context, intent: Intent) {
        try {
            super.onReceive(context, intent)
            val action = intent.action
            com.example.LogKeeper.log("onReceive action: $action", "MediaWidgetProvider")
            
        if (action == "ACTION_REFRESH") {
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
            appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetManager.getAppWidgetIds(componentName), R.id.widget_list)
        } else if (action == "ACTION_OPEN_APP") {
            val appIntent = android.content.Intent(context, com.example.MainActivity::class.java).apply {
                this.action = "com.example.ACTION_OPEN_PLAYER"
                flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            context.startActivity(appIntent)
        } else if (action == "ACTION_PIP") {
            val appIntent = android.content.Intent(context, com.example.MainActivity::class.java).apply {
                this.action = "com.example.ACTION_START_PIP"
                flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            context.startActivity(appIntent)
        } else if (action in listOf("ACTION_PLAY_PAUSE", "ACTION_PREV", "ACTION_NEXT", "ACTION_LOOP", "ACTION_SHUFFLE", "ACTION_MINIPLAYER", "ACTION_CLOSE")) {
            val serviceIntent = Intent("com.example.ACTION_WIDGET_COMMAND")
            serviceIntent.setPackage(context.packageName)
            serviceIntent.putExtra("command", action)
            context.sendBroadcast(serviceIntent)
        } else if (action == "ACTION_PLAY_ITEM") {
            val widgetAction = intent.getStringExtra("WIDGET_ACTION")
            val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
            if (widgetAction == "OPEN_FOLDER") {
                val folderId = intent.getStringExtra("FOLDER_ID")
                prefs.edit().putString("folder_id", folderId).apply()
                appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetManager.getAppWidgetIds(componentName), R.id.widget_list)
            } else if (widgetAction == "BACK_FOLDER") {
                prefs.edit().putString("folder_id", null).apply()
                appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetManager.getAppWidgetIds(componentName), R.id.widget_list)
            } else if (widgetAction == "PLAY_FILE") {
                val uriStr = intent.getStringExtra("MEDIA_URI")
                val serviceIntent = Intent("com.example.ACTION_WIDGET_COMMAND")
                serviceIntent.setPackage(context.packageName)
                serviceIntent.putExtra("command", "ACTION_PLAY_FILE")
                serviceIntent.putExtra("uri", uriStr)
                context.sendBroadcast(serviceIntent)
            } else if (widgetAction == "PLAYLIST_ITEM") {
                val index = intent.getIntExtra("EXTRA_INDEX", 0)
                val serviceIntent = Intent("com.example.ACTION_WIDGET_COMMAND")
                serviceIntent.setPackage(context.packageName)
                serviceIntent.putExtra("command", "ACTION_PLAY_ITEM")
                serviceIntent.putExtra("index", index)
                context.sendBroadcast(serviceIntent)
            } else {
                // Fallback for older intents
                val index = intent.getIntExtra("EXTRA_INDEX", 0)
                val serviceIntent = Intent("com.example.ACTION_WIDGET_COMMAND")
                serviceIntent.setPackage(context.packageName)
                serviceIntent.putExtra("command", "ACTION_PLAY_ITEM")
                serviceIntent.putExtra("index", index)
                context.sendBroadcast(serviceIntent)
            }
        }
        } catch (e: Exception) {
            com.example.LogKeeper.logError("MediaWidgetProvider", "Error in onReceive", e)
        }
    }"""

replacement = """    override fun onReceive(context: Context, intent: Intent) {
        val action = intent.action
        com.example.LogKeeper.log("onReceive action: $action", "MediaWidgetProvider")
        
        if (action == "ACTION_REFRESH" || action == "android.appwidget.action.APPWIDGET_UPDATE" || action == "android.appwidget.action.APPWIDGET_UPDATE_OPTIONS" || action == "android.appwidget.action.APPWIDGET_ENABLED") {
            super.onReceive(context, intent)
            if (action == "ACTION_REFRESH") {
                val appWidgetManager = AppWidgetManager.getInstance(context)
                val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
                appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetManager.getAppWidgetIds(componentName), R.id.widget_list)
            }
            return
        }
        
        if (action == "ACTION_OPEN_APP") {
            val appIntent = android.content.Intent(context, com.example.MainActivity::class.java).apply {
                this.action = "com.example.ACTION_OPEN_PLAYER"
                flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            context.startActivity(appIntent)
            return
        }
        
        if (action == "ACTION_PIP") {
            val appIntent = android.content.Intent(context, com.example.MainActivity::class.java).apply {
                this.action = "com.example.ACTION_START_PIP"
                flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            context.startActivity(appIntent)
            return
        }
        
        val widgetAction = intent.getStringExtra("WIDGET_ACTION")
        if (action == "ACTION_PLAY_ITEM") {
            if (widgetAction == "OPEN_FOLDER" || widgetAction == "BACK_FOLDER") {
                val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
                val appWidgetManager = AppWidgetManager.getInstance(context)
                val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
                if (widgetAction == "OPEN_FOLDER") {
                    val folderId = intent.getStringExtra("FOLDER_ID")
                    prefs.edit().putString("folder_id", folderId).apply()
                } else {
                    prefs.edit().putString("folder_id", null).apply()
                }
                appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetManager.getAppWidgetIds(componentName), R.id.widget_list)
                return
            }
        }

        // Media controller commands
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
                        // also send broadcast to close service
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
                    
                    val appWidgetManager = AppWidgetManager.getInstance(context)
                    val componentName = android.content.ComponentName(context, MediaWidgetProvider::class.java)
                    appWidgetManager.notifyAppWidgetViewDataChanged(appWidgetManager.getAppWidgetIds(componentName), R.id.widget_list)
                    
                    androidx.media3.session.MediaController.releaseFuture(controllerFuture)
                } catch (e: Exception) {
                    com.example.LogKeeper.logError("MediaWidgetProvider", "Error in MediaController", e)
                } finally {
                    pendingResult.finish()
                }
            }, androidx.core.content.ContextCompat.getMainExecutor(context))
        } else {
            // Unhandled intents
            super.onReceive(context, intent)
        }
    }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target not found.")
