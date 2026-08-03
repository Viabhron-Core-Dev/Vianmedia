with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    "@Suppress(\"DEPRECATION\")\n                @Suppress(\"DEPRECATION\")",
    "@Suppress(\"DEPRECATION\")"
)

with open("app/src/main/java/com/example/ui/screens/PlayerScreen.kt", "w") as f:
    f.write(content)
