import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

old_listener = """                    override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
                        if (videoSize.width > 0 && videoSize.height > 0) {
                            videoWidth = videoSize.width
                            videoHeight = videoSize.height
                        }
                    }"""

new_listener = """                    override fun onVideoSizeChanged(videoSize: androidx.media3.common.VideoSize) {
                        if (videoSize.width > 0 && videoSize.height > 0) {
                            if (videoSize.unappliedRotationDegrees == 90 || videoSize.unappliedRotationDegrees == 270) {
                                videoWidth = videoSize.height
                                videoHeight = videoSize.width
                            } else {
                                videoWidth = videoSize.width
                                videoHeight = videoSize.height
                            }
                        }
                    }"""

content = content.replace(old_listener, new_listener)

# Wait, in export we used `exoPlayer?.videoSize?.width` and `height`.
# We should use `videoWidth` and `videoHeight` instead!
old_res = """                            val originalW = exoPlayer?.videoSize?.width ?: 1
                            val originalH = exoPlayer?.videoSize?.height ?: 1"""
new_res = """                            val originalW = videoWidth
                            val originalH = videoHeight"""

content = content.replace(old_res, new_res)

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)
print("Fixed rotation handling")
