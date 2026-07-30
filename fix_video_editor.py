import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

target1 = """    var isConverting by remember { mutableStateOf(false) }"""
replacement1 = """    var isConverting by remember { mutableStateOf(false) }
    var exportedPreviewUri by remember { mutableStateOf<String?>(null) }
    var wasExporting by remember { mutableStateOf(false) }
    
    LaunchedEffect(com.example.service.FFmpegStatus.isRunning) {
        if (com.example.service.FFmpegStatus.isRunning) {
            wasExporting = true
        } else if (wasExporting) {
            wasExporting = false
            if (com.example.service.FFmpegStatus.lastOutputUri != null) {
                exportedPreviewUri = com.example.service.FFmpegStatus.lastOutputUri
            }
        }
    }
"""

if target1 in content:
    content = content.replace(target1, replacement1)
    
target2 = """            )
        }
    }
}

@Composable
fun ToolIcon"""
replacement2 = """            )
        }
        
        if (exportedPreviewUri != null) {
            androidx.compose.ui.window.Dialog(onDismissRequest = { exportedPreviewUri = null }) {
                Card(shape = RoundedCornerShape(16.dp)) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text("Export Complete!", style = MaterialTheme.typography.titleMedium)
                        Spacer(modifier = Modifier.height(16.dp))
                        // Mini player for portrait
                        Box(modifier = Modifier.width(200.dp).height(300.dp).background(androidx.compose.ui.graphics.Color.Black)) {
                            var previewPlayer by remember { mutableStateOf<androidx.media3.exoplayer.ExoPlayer?>(null) }
                            DisposableEffect(exportedPreviewUri) {
                                val p = androidx.media3.exoplayer.ExoPlayer.Builder(context).build()
                                p.setMediaItem(androidx.media3.common.MediaItem.fromUri(Uri.parse(exportedPreviewUri!!)))
                                p.prepare()
                                p.playWhenReady = true
                                p.repeatMode = androidx.media3.common.Player.REPEAT_MODE_ALL
                                previewPlayer = p
                                onDispose { p.release() }
                            }
                            if (previewPlayer != null) {
                                androidx.compose.ui.viewinterop.AndroidView(
                                    factory = { ctx ->
                                        androidx.media3.ui.PlayerView(ctx).apply {
                                            player = previewPlayer
                                            useController = false
                                            resizeMode = androidx.media3.ui.AspectRatioFrameLayout.RESIZE_MODE_FIT
                                        }
                                    },
                                    modifier = Modifier.fillMaxSize()
                                )
                            }
                        }
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(onClick = {
                            val newUri = exportedPreviewUri
                            exportedPreviewUri = null
                            val intent = android.content.Intent(context, com.example.EditMediaActivity::class.java).apply {
                                action = android.content.Intent.ACTION_EDIT
                                setDataAndType(Uri.parse(newUri), "video/*")
                            }
                            context.startActivity(intent)
                            (context as? android.app.Activity)?.finish()
                        }, modifier = Modifier.fillMaxWidth()) {
                            Text("Edit Finished File")
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        TextButton(onClick = { exportedPreviewUri = null }, modifier = Modifier.fillMaxWidth()) {
                            Text("Dismiss")
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ToolIcon"""

if target2 in content:
    content = content.replace(target2, replacement2)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Replaced")
else:
    print("Target not found")
