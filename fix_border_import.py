with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

import_statement = "import androidx.compose.foundation.border\n"
if import_statement not in content:
    content = content.replace("import androidx.compose.foundation.background\n", "import androidx.compose.foundation.background\n" + import_statement)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
