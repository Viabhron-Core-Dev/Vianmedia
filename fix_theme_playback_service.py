import re

with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    content = f.read()

content = content.replace("            com.example.ui.components.MiniPlayerOverlay(",
"""            com.example.ui.theme.MyApplicationTheme {
                com.example.ui.components.MiniPlayerOverlay(""")

content = content.replace("                onResize = {\n                    // Handled within overlay\n                }\n            )",
"""                onResize = {
                    // Handled within overlay
                }
            )
            }""")

with open("app/src/main/java/com/example/service/PlaybackService.kt", "w") as f:
    f.write(content)
