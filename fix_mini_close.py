with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

target = """                        context.startActivity(intent)
                        onClose()
                    }, modifier = Modifier.size(32.dp)) {"""

replacement = """                        context.startActivity(intent)
                        onMinimize()
                    }, modifier = Modifier.size(32.dp)) {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
