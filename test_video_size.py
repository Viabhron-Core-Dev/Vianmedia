with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

# Let's see where exoPlayer is defined
lines = content.split('\n')
for i, line in enumerate(lines):
    if "exoPlayer" in line and "remember" in line:
        print(f"{i}: {line}")
