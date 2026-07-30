with open("app/src/main/java/com/example/widget/WidgetSearchActivity.kt", "r") as f:
    content = f.read()

target = "Icon(androidx.compose.material.icons.filled.Search, \"Search\")"
replacement = "Icon(androidx.compose.material.icons.Icons.Default.Search, \"Search\")"

if target in content:
    content = content.replace(target, replacement)

import_target = "import androidx.compose.ui.window.Dialog"
import_replacement = "import androidx.compose.ui.window.Dialog\nimport androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.filled.Search"

content = content.replace(import_target, import_replacement)

with open("app/src/main/java/com/example/widget/WidgetSearchActivity.kt", "w") as f:
    f.write(content)
print("Replaced successfully.")
