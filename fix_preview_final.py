with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

old_block = """                val ratio = if (editState.cropRect == "Center Crop" && currentTool != VideoEditorTool.CROP) {
                    1f
                } else {
                    when (editState.aspectRatio) {
                        "16:9" -> 16f / 9f
                        "9:16" -> 9f / 16f
                        "1:1" -> 1f
                        "4:3" -> 4f / 3f
                        "21:9" -> 21f / 9f
                        else -> null
                    }
                }
                val previewModifier = if (ratio != null) {
                    Modifier
                        .aspectRatio(ratio)
                        .background(Color.DarkGray)
                } else {
                    Modifier.fillMaxSize()
                }"""

new_block = """                val ratio = if (editState.cropRect == "Center Crop" && currentTool != VideoEditorTool.CROP) {
                    1f
                } else {
                    when (editState.aspectRatio) {
                        "16:9" -> 16f / 9f
                        "9:16" -> 9f / 16f
                        "1:1" -> 1f
                        "4:3" -> 4f / 3f
                        "21:9" -> 21f / 9f
                        else -> if (videoWidth > 0 && videoHeight > 0) videoWidth.toFloat() / videoHeight.toFloat() else 16f/9f
                    }
                }
                val previewModifier = Modifier
                    .aspectRatio(ratio)
                    .background(Color.DarkGray)"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Fixed ratio logic")
else:
    print("Could not find block")
