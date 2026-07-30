with open("app/src/main/java/com/example/service/FFmpegService.kt", "r") as f:
    content = f.read()

target = """object FFmpegStatus {
    var isRunning by mutableStateOf(false)
    var totalFiles by mutableStateOf(0)
    var currentFile by mutableStateOf(0)
    var currentProgress by mutableStateOf("")
}"""
replacement = """object FFmpegStatus {
    var isRunning by mutableStateOf(false)
    var totalFiles by mutableStateOf(0)
    var currentFile by mutableStateOf(0)
    var currentProgress by mutableStateOf("")
    var lastOutputUri by mutableStateOf<String?>(null)
}"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/service/FFmpegService.kt", "w") as f:
    f.write(content)
print("Replaced status")
