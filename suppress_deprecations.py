import re

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    "val w = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.width else videoSize.height",
    "@Suppress(\"DEPRECATION\")\n                val w = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.width else videoSize.height"
)
content = content.replace(
    "val h = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.height else videoSize.width",
    "@Suppress(\"DEPRECATION\")\n                val h = if (videoSize.unappliedRotationDegrees % 180 == 0) videoSize.height else videoSize.width"
)

content = content.replace(
    "val w = if (vs.unappliedRotationDegrees % 180 == 0) vs.width else vs.height",
    "@Suppress(\"DEPRECATION\")\n                    val w = if (vs.unappliedRotationDegrees % 180 == 0) vs.width else vs.height"
)
content = content.replace(
    "val h = if (vs.unappliedRotationDegrees % 180 == 0) vs.height else vs.width",
    "@Suppress(\"DEPRECATION\")\n                    val h = if (vs.unappliedRotationDegrees % 180 == 0) vs.height else vs.width"
)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
