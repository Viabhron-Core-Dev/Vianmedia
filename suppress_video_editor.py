import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    "if (videoSize.unappliedRotationDegrees == 90 || videoSize.unappliedRotationDegrees == 270) {",
    "@Suppress(\"DEPRECATION\")\n                            if (videoSize.unappliedRotationDegrees == 90 || videoSize.unappliedRotationDegrees == 270) {"
)

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)
