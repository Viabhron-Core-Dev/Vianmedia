import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    "val effectiveVideoWidth = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) videoHeight else videoWidth",
    "val effectiveVideoWidth = videoWidth"
)

content = content.replace(
    "val effectiveVideoHeight = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) videoWidth else videoHeight",
    "val effectiveVideoHeight = videoHeight"
)

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)
