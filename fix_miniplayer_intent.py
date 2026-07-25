with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

target = """                    IconButton(onClick = {
                        val intent = android.content.Intent(context, com.example.MainActivity::class.java).apply {
                            flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_SINGLE_TOP
                        }
                        context.startActivity(intent)
                        onClose()
                    }, modifier = Modifier.size(32.dp)) {"""

replacement = """                    IconButton(onClick = {
                        val intent = android.content.Intent(context, com.example.MainActivity::class.java).apply {
                            action = "com.example.ACTION_OPEN_PLAYER"
                            flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_SINGLE_TOP or android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP
                        }
                        context.startActivity(intent)
                        onClose()
                    }, modifier = Modifier.size(32.dp)) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
