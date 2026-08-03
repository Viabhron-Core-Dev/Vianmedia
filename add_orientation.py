import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

# Add state variable
state_var_addition = """        var format by remember { mutableStateOf("mp4") }
        var exportOrientation by remember { mutableStateOf("Auto") }"""
content = content.replace('        var format by remember { mutableStateOf("mp4") }', state_var_addition)

# Add UI for it
ui_addition = """                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(checked = fastExport, onCheckedChange = { fastExport = it })
                            Text("Fast Export (ultrafast preset)")
                        }
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Export Orientation")
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                            FilterChip(selected = exportOrientation == "Auto", onClick = { exportOrientation = "Auto" }, label= { Text("Auto")})
                            FilterChip(selected = exportOrientation == "Portrait", onClick = { exportOrientation = "Portrait" }, label= { Text("Portrait")})
                            FilterChip(selected = exportOrientation == "Landscape", onClick = { exportOrientation = "Landscape" }, label= { Text("Landscape")})
                        }"""
content = content.replace("""                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(checked = fastExport, onCheckedChange = { fastExport = it })
                            Text("Fast Export (ultrafast preset)")
                        }""", ui_addition)

# Update logic
old_portrait_logic = """                            val isPortrait = when {
                                editState.aspectRatio == "9:16" -> true
                                editState.aspectRatio == "16:9" -> false
                                editState.aspectRatio == "4:3" -> false
                                editState.aspectRatio == "21:9" -> false
                                editState.aspectRatio == "1:1" -> false
                                editState.cropRect == "Custom" -> {
                                    val cw = rotatedW * (editState.cropRight - editState.cropLeft)
                                    val ch = rotatedH * (editState.cropBottom - editState.cropTop)
                                    ch > cw
                                }
                                editState.cropRect == "Center Crop" -> false
                                else -> rotatedH > rotatedW
                            }"""

new_portrait_logic = """                            val isPortrait = when (exportOrientation) {
                                "Portrait" -> true
                                "Landscape" -> false
                                else -> when {
                                    editState.aspectRatio == "9:16" -> true
                                    editState.aspectRatio == "16:9" -> false
                                    editState.aspectRatio == "4:3" -> false
                                    editState.aspectRatio == "21:9" -> false
                                    editState.aspectRatio == "1:1" -> false
                                    editState.cropRect == "Custom" -> {
                                        val cw = rotatedW * (editState.cropRight - editState.cropLeft)
                                        val ch = rotatedH * (editState.cropBottom - editState.cropTop)
                                        ch > cw
                                    }
                                    editState.cropRect == "Center Crop" -> false
                                    else -> rotatedH > rotatedW
                                }
                            }"""
content = content.replace(old_portrait_logic, new_portrait_logic)

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)
