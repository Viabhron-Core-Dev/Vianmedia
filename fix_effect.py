import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = "LaunchedEffect(editState.rotateConfig, editState.cropRect, cropLeftKey, cropRightKey, cropTopKey, cropBottomKey, editState.aspectRatio, currentTool) {"
replacement = "LaunchedEffect(exoPlayer, editState.rotateConfig, editState.cropRect, cropLeftKey, cropRightKey, cropTopKey, cropBottomKey, editState.aspectRatio, currentTool) {"

if target in content:
    content = content.replace(target, replacement)
    print("Success")
    
with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
