import sys

with open('app/src/main/java/com/example/ui/components/FloatingVideoPlayerOverlay.kt', 'r') as f:
    content = f.read()

target1 = """    var title by remember { mutableStateOf(player?.currentMediaItem?.mediaMetadata?.title?.toString() ?: "Unknown") }
    var isPlaying by remember { mutableStateOf(player?.isPlaying == true) }"""

replacement1 = """    var title by remember { mutableStateOf(player?.currentMediaItem?.mediaMetadata?.title?.toString() ?: "Unknown") }
    var isPlaying by remember { mutableStateOf(player?.isPlaying == true) }
    val context = androidx.compose.ui.platform.LocalContext.current
    val settingsManager = remember { com.example.data.SettingsManager.getInstance(context) }
    val keepScreenAwake by settingsManager.keepScreenAwake.androidx.compose.runtime.collectAsState()"""

if target1 in content:
    content = content.replace(target1, replacement1)
    print("Success 1")

target2 = """                if (player != null) {
                    AndroidView(
                        factory = { ctx ->
                            PlayerView(ctx).apply {
                                this.player = player
                                useController = false
                            }
                        },
                        modifier = Modifier.fillMaxSize().pointerInput(Unit) {
                            detectTapGestures(
                                onTap = { showControls = !showControls }
                            )
                        }
                    )"""

replacement2 = """                if (player != null) {
                    AndroidView(
                        factory = { ctx ->
                            PlayerView(ctx).apply {
                                this.player = player
                                useController = false
                            }
                        },
                        update = { view ->
                            view.keepScreenOn = keepScreenAwake && isPlaying
                        },
                        modifier = Modifier.fillMaxSize().pointerInput(Unit) {
                            detectTapGestures(
                                onTap = { showControls = !showControls }
                            )
                        }
                    )"""

if target2 in content:
    content = content.replace(target2, replacement2)
    print("Success 2")

with open('app/src/main/java/com/example/ui/components/FloatingVideoPlayerOverlay.kt', 'w') as f:
    f.write(content)
