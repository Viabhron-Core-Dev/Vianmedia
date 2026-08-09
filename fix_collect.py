import sys

with open('app/src/main/java/com/example/ui/components/FloatingVideoPlayerOverlay.kt', 'r') as f:
    content = f.read()

content = content.replace(
    "settingsManager.keepScreenAwake.androidx.compose.runtime.collectAsState()",
    "settingsManager.keepScreenAwake.collectAsState()"
)

with open('app/src/main/java/com/example/ui/components/FloatingVideoPlayerOverlay.kt', 'w') as f:
    f.write(content)
