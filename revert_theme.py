import re
with open("app/src/main/java/com/example/ui/theme/Theme.kt", "r") as f:
    content = f.read()

pattern = r"    onPrimaryContainer = LightBlueOnPrimaryContainer,\n    surfaceContainerLowest = androidx\.compose\.ui\.graphics\.Color\.White,\n    surfaceContainerLow = androidx\.compose\.ui\.graphics\.Color\.White,\n    surfaceContainer = androidx\.compose\.ui\.graphics\.Color\.White,\n    surfaceContainerHigh = androidx\.compose\.ui\.graphics\.Color\.White,\n    surfaceContainerHighest = androidx\.compose\.ui\.graphics\.Color\.White"
replacement = "    onPrimaryContainer = LightBlueOnPrimaryContainer"
content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "w") as f:
    f.write(content)
