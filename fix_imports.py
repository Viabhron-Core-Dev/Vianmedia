import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.layout.layout\nimport androidx.compose.ui.unit.Constraints")

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)
