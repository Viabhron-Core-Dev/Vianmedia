import sys

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'r') as f:
    content = f.read()

target1 = "    val settingsManager = com.example.data.SettingsManager.getInstance(context)"
replacement1 = """    val settingsManager = com.example.data.SettingsManager.getInstance(context)
    val keepScreenAwake by settingsManager.keepScreenAwake.collectAsState()"""
if target1 in content:
    content = content.replace(target1, replacement1)
    print("Success 1")

target2 = """            update = { view ->
                view.player = mediaController
                view.resizeMode = resizeMode"""
replacement2 = """            update = { view ->
                view.player = mediaController
                view.resizeMode = resizeMode
                view.keepScreenOn = keepScreenAwake && isPlaying"""
if target2 in content:
    content = content.replace(target2, replacement2)
    print("Success 2")

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'w') as f:
    f.write(content)
