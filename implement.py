import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

# Fix updateOrientation
old_update = """        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
            if (videoSize.width > 0 && videoSize.height > 0) {
                val isPortrait = videoSize.height > videoSize.width
                context.findActivity()?.requestedOrientation = if (isPortrait) {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                } else {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                }
            }
        }"""

new_update = """        fun updateOrientation(videoSize: androidx.media3.common.VideoSize) {
            if (videoSize.width > 0 && videoSize.height > 0) {
                @Suppress("DEPRECATION")
                val w = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.width else videoSize.height
                @Suppress("DEPRECATION")
                val h = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.height else videoSize.width
                val isPortrait = h > w
                context.findActivity()?.requestedOrientation = if (isPortrait) {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                } else {
                    android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                }
            }
        }"""
content = content.replace(old_update, new_update)

# Fix onEvents video size check
old_events = """            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_VIDEO_SIZE_CHANGED)) {
                    updateOrientation(player.videoSize)
                }
            }"""

new_events = """            override fun onEvents(player: androidx.media3.common.Player, events: androidx.media3.common.Player.Events) {
                if (events.contains(androidx.media3.common.Player.EVENT_VIDEO_SIZE_CHANGED) || events.contains(androidx.media3.common.Player.EVENT_MEDIA_ITEM_TRANSITION)) {
                    updateOrientation(player.videoSize)
                }
            }"""
content = content.replace(old_events, new_events)

# Fix PiP click listener
old_pip_button = """                                IconButton(modifier = Modifier.size(36.dp), onClick = {
                                    val appOps = context.getSystemService(android.content.Context.APP_OPS_SERVICE) as android.app.AppOpsManager
                                    val mode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                                        appOps.unsafeCheckOpNoThrow(android.app.AppOpsManager.OPSTR_PICTURE_IN_PICTURE, android.os.Process.myUid(), context.packageName)
                                    } else {
                                        appOps.checkOpNoThrow(android.app.AppOpsManager.OPSTR_PICTURE_IN_PICTURE, android.os.Process.myUid(), context.packageName)
                                    }
                                    
                                    if (mode != android.app.AppOpsManager.MODE_ALLOWED) {
                                        com.example.LogKeeper.log("PiP permission not granted, redirecting to settings", "PlayerScreen")
                                        val intent = android.content.Intent("android.settings.PICTURE_IN_PICTURE_SETTINGS").apply {
                                            data = android.net.Uri.fromParts("package", context.packageName, null)
                                        }
                                        try {
                                            context.startActivity(intent)
                                        } catch (e: Exception) {
                                            com.example.LogKeeper.logError("PlayerScreen", "Could not open PiP settings", e)
                                        }
                                    } else {
                                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                            try {
                                                val width = mediaController?.videoSize?.width ?: 0
                                                val height = mediaController?.videoSize?.height ?: 0
                                                val params = PipHelper.buildPipParams(context, mediaController, width, height)
                                                val activity = context.findActivity()
                                                if (activity != null) {
                                                    val entered = activity.enterPictureInPictureMode(params)
                                                    com.example.LogKeeper.log("PiP enter result: $entered", "PlayerScreen")
                                                    if (!entered) {
                                                        com.example.LogKeeper.logError("PlayerScreen", "enterPictureInPictureMode returned false", null)
                                                    }
                                                } else {
                                                    com.example.LogKeeper.logError("PlayerScreen", "Activity is null for PiP", null)
                                                }
                                            } catch (e: Exception) {
                                                com.example.LogKeeper.logError("PlayerScreen", "Exception entering PiP", e)
                                            }
                                        } else {
                                            com.example.LogKeeper.logError("PlayerScreen", "PiP not supported on this SDK", null)
                                        }
                                    }
                                }) {"""

new_pip_button = """                                IconButton(modifier = Modifier.size(36.dp), onClick = {
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                        try {
                                            val vs = mediaController?.videoSize
                                            val rot = vs?.unappliedRotationDegrees ?: 0
                                            @Suppress("DEPRECATION")
                                            val width = if (rot % 180 == 0) vs?.width ?: 0 else vs?.height ?: 0
                                            @Suppress("DEPRECATION")
                                            val height = if (rot % 180 == 0) vs?.height ?: 0 else vs?.width ?: 0
                                            val params = PipHelper.buildPipParams(context, mediaController, width, height)
                                            val activity = context.findActivity()
                                            
                                            var entered = false
                                            if (activity != null) {
                                                entered = activity.enterPictureInPictureMode(params)
                                            }
                                            
                                            if (!entered) {
                                                val intent = android.content.Intent("android.settings.PICTURE_IN_PICTURE_SETTINGS").apply {
                                                    data = android.net.Uri.fromParts("package", context.packageName, null)
                                                }
                                                context.startActivity(intent)
                                            }
                                        } catch (e: Exception) {
                                            try {
                                                val intent = android.content.Intent("android.settings.PICTURE_IN_PICTURE_SETTINGS").apply {
                                                    data = android.net.Uri.fromParts("package", context.packageName, null)
                                                }
                                                context.startActivity(intent)
                                            } catch (e2: Exception) {
                                                com.example.LogKeeper.logError("PlayerScreen", "Could not open PiP settings", e2)
                                            }
                                        }
                                    }
                                }) {"""
content = content.replace(old_pip_button, new_pip_button)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    overlay_content = f.read()

old_overlay_pip = """                    IconButton(onClick = {
                        val appOps = context.getSystemService(android.content.Context.APP_OPS_SERVICE) as android.app.AppOpsManager
                        val mode = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.Q) {
                            appOps.unsafeCheckOpNoThrow(android.app.AppOpsManager.OPSTR_PICTURE_IN_PICTURE, android.os.Process.myUid(), context.packageName)
                        } else {
                            appOps.checkOpNoThrow(android.app.AppOpsManager.OPSTR_PICTURE_IN_PICTURE, android.os.Process.myUid(), context.packageName)
                        }
                        if (mode == android.app.AppOpsManager.MODE_ALLOWED) {
                            val activity = context as? android.app.Activity ?: (context as? android.content.ContextWrapper)?.baseContext as? android.app.Activity
                            activity?.enterPictureInPictureMode(android.app.PictureInPictureParams.Builder().build())
                        } else {
                            android.widget.Toast.makeText(context, "PiP permission not granted", android.widget.Toast.LENGTH_SHORT).show()
                        }
                    }, modifier = Modifier.size(32.dp)) {"""

new_overlay_pip = """                    IconButton(onClick = {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                            val activity = context as? android.app.Activity ?: (context as? android.content.ContextWrapper)?.baseContext as? android.app.Activity
                            var entered = false
                            try {
                                if (activity != null) {
                                    entered = activity.enterPictureInPictureMode(android.app.PictureInPictureParams.Builder().build())
                                }
                            } catch (e: Exception) { }
                            
                            if (!entered) {
                                try {
                                    val intent = android.content.Intent("android.settings.PICTURE_IN_PICTURE_SETTINGS").apply {
                                        data = android.net.Uri.fromParts("package", context.packageName, null)
                                    }
                                    context.startActivity(intent)
                                } catch (e: Exception) {
                                    android.widget.Toast.makeText(context, "PiP not available", android.widget.Toast.LENGTH_SHORT).show()
                                }
                            }
                        }
                    }, modifier = Modifier.size(32.dp)) {"""
overlay_content = overlay_content.replace(old_overlay_pip, new_overlay_pip)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(overlay_content)
