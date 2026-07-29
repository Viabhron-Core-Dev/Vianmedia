with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

target = """                                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                        Text(formatMs(start.toLong()), style = MaterialTheme.typography.labelMedium)
                                        Text(formatMs(end.toLong()), style = MaterialTheme.typography.labelMedium)
                                    }"""

replacement = """                                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                        Text(formatMs(start.toLong()), style = MaterialTheme.typography.labelMedium)
                                        
                                        var customCutText by remember { mutableStateOf("") }
                                        androidx.compose.foundation.text.BasicTextField(
                                            value = if (customCutText.isEmpty()) "Cut: ${formatMs((end - start).toLong())}" else customCutText,
                                            onValueChange = { customCutText = it },
                                            textStyle = MaterialTheme.typography.labelMedium.copy(
                                                color = MaterialTheme.colorScheme.primary,
                                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                                            ),
                                            modifier = Modifier.weight(1f).padding(horizontal = 8.dp)
                                        )
                                        
                                        Text(formatMs(end.toLong()), style = MaterialTheme.typography.labelMedium)
                                    }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Replaced Row successfully.")
else:
    print("Target Row not found.")
