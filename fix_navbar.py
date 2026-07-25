with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

target = """            if (showControls && !isInPipMode) {
                insetsController.show(androidx.core.view.WindowInsetsCompat.Type.statusBars())
                insetsController.hide(androidx.core.view.WindowInsetsCompat.Type.navigationBars())
            } else {"""

replacement = """            if (showControls && !isInPipMode) {
                insetsController.show(androidx.core.view.WindowInsetsCompat.Type.systemBars())
            } else {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
