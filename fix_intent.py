import re

with open("app/src/main/java/com/example/ui/screens/PhotoEditorScreen.kt", "r") as f:
    content = f.read()

old_intent = """                        val intent = android.content.Intent(context, com.example.service.CompressionService::class.java).apply {
                            putStringArrayListExtra("uris", java.util.ArrayList(listOf(editedUri)))
                            putExtra("maxWidth", w)
                            putExtra("maxHeight", h)
                        }"""

new_intent = """                        val intent = android.content.Intent(context, com.example.service.CompressionService::class.java).apply {
                            putStringArrayListExtra("uris", java.util.ArrayList(listOf(editedUri)))
                            putExtra("maxWidth", w)
                            putExtra("maxHeight", h)
                            putExtra("quality", q)
                            putExtra("format", f)
                        }"""

content = content.replace(old_intent, new_intent)

with open("app/src/main/java/com/example/ui/screens/PhotoEditorScreen.kt", "w") as f:
    f.write(content)
