import re
with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

target = """    LaunchedEffect(com.example.service.FFmpegStatus.isRunning) {
        if (com.example.service.FFmpegStatus.isRunning) {
            wasFFmpegRunning = true
        } else if (wasFFmpegRunning) {
            wasFFmpegRunning = false
            android.widget.Toast.makeText(context, "Media processing complete!", android.widget.Toast.LENGTH_SHORT).show()
            if (initialUris.isNotEmpty()) {
                (context as? android.app.Activity)?.finish()
            }
        }
    }"""
replacement = """    LaunchedEffect(com.example.service.FFmpegStatus.isRunning) {
        if (com.example.service.FFmpegStatus.isRunning) {
            wasFFmpegRunning = true
        } else if (wasFFmpegRunning) {
            wasFFmpegRunning = false
            android.widget.Toast.makeText(context, "Media processing complete!", android.widget.Toast.LENGTH_SHORT).show()
            // Do not auto-finish here so VideoEditor can show the preview dialog.
            // If it's batch compression, they can dismiss the modal.
        }
    }"""
if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "w") as f:
        f.write(content)
    print("Replaced")
else:
    print("Target not found")
