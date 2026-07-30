import re
with open("app/src/main/java/com/example/service/FFmpegService.kt", "r") as f:
    content = f.read()

target = """        FFmpegStatus.isRunning = true
        FFmpegStatus.totalFiles = uris.size"""
replacement = """        FFmpegStatus.isRunning = true
        FFmpegStatus.lastOutputUri = null
        FFmpegStatus.totalFiles = uris.size"""
if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/service/FFmpegService.kt", "w") as f:
        f.write(content)
    print("Replaced!")
else:
    print("Not found.")
