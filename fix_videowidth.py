import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target1 = """    var videoWidth by remember { mutableIntStateOf(1) }
    var videoHeight by remember { mutableIntStateOf(1) }
    val exoPlayer = remember(effectiveUri) {"""

replacement1 = """    var videoWidth by remember { mutableIntStateOf(1) }
    var videoHeight by remember { mutableIntStateOf(1) }
    var currentVideoUri by remember { mutableStateOf<String?>(null) }
    
    if (currentVideoUri != effectiveUri.toString()) {
        currentVideoUri = effectiveUri.toString()
        videoWidth = 1
        videoHeight = 1
    }
    
    val exoPlayer = remember(effectiveUri) {"""

if target1 in content:
    content = content.replace(target1, replacement1)
    print("Success 1")

target2 = """                    override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
                        if (videoSize.width > 0 && videoSize.height > 0) {
                            @Suppress("DEPRECATION")
                            if (videoSize.unappliedRotationDegrees == 90 || videoSize.unappliedRotationDegrees == 270) {
                                videoWidth = videoSize.height
                                videoHeight = videoSize.width
                            } else {
                                videoWidth = videoSize.width
                                videoHeight = videoSize.height
                            }
                        }
                    }"""

replacement2 = """                    override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
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
                    }"""

if content.count(target2) > 0:
    content = content.replace(target2, replacement2)
    print("Success 2")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)

