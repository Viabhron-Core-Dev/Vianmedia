with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

target1 = """    var isExpanded by remember { mutableStateOf(false) }"""
content = content.replace(target1, "")

target2 = """                    IconButton(onClick = { isExpanded = !isExpanded }) {
                        Icon(if (isExpanded) Icons.Filled.ExpandLess else Icons.Filled.ExpandMore, "Toggle Playlist", tint = MaterialTheme.colorScheme.onSurface)
                    }"""
content = content.replace(target2, "")

target3 = """            if (isExpanded) {"""
replacement3 = """            if (true) {"""
content = content.replace(target3, replacement3)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
