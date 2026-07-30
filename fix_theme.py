import re

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "r") as f:
    content = f.read()

pattern = r"private val LightBlueColorScheme = lightColorScheme\([\s\S]*?onPrimaryContainer = LightBlueOnPrimaryContainer\n\)"

replacement = """private val LightBlueColorScheme = lightColorScheme(
    primary = LightBluePrimary,
    onPrimary = LightBlueOnPrimary,
    background = LightBlueBackground,
    onBackground = LightBlueOnBackground,
    surface = LightBlueSurface,
    onSurface = LightBlueOnSurface,
    surfaceVariant = LightBlueSurfaceVariant,
    onSurfaceVariant = LightBlueOnSurfaceVariant,
    primaryContainer = LightBluePrimaryContainer,
    onPrimaryContainer = LightBlueOnPrimaryContainer,
    surfaceContainerLowest = androidx.compose.ui.graphics.Color.White,
    surfaceContainerLow = androidx.compose.ui.graphics.Color.White,
    surfaceContainer = androidx.compose.ui.graphics.Color.White,
    surfaceContainerHigh = androidx.compose.ui.graphics.Color.White,
    surfaceContainerHighest = androidx.compose.ui.graphics.Color.White
)"""

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "w") as f:
    f.write(content)
print("Updated Theme")
