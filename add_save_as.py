with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "r") as f:
    content = f.read()

target = """                navigationIcon = {
                    if (isMultiSelectMode) {
                        IconButton(onClick = { selectedItems.clear() }) {
                            Icon(Icons.Filled.Close, contentDescription = "Clear Selection")
                        }
                    } else {
                        IconButton(onClick = onNavigateBack) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    }
                }
            )
        },"""

replacement = """                navigationIcon = {
                    if (isMultiSelectMode) {
                        IconButton(onClick = { selectedItems.clear() }) {
                            Icon(Icons.Filled.Close, contentDescription = "Clear Selection")
                        }
                    } else {
                        IconButton(onClick = onNavigateBack) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    }
                },
                actions = {
                    if (!isMultiSelectMode && playlist?.name == "Temp Current") {
                        var showSaveDialog by remember { mutableStateOf(false) }
                        TextButton(onClick = { showSaveDialog = true }) {
                            Text("Save As")
                        }
                        
                        if (showSaveDialog) {
                            var newName by remember { mutableStateOf("") }
                            AlertDialog(
                                onDismissRequest = { showSaveDialog = false },
                                title = { Text("Save Playlist As") },
                                text = {
                                    OutlinedTextField(
                                        value = newName,
                                        onValueChange = { newName = it },
                                        label = { Text("Playlist Name") },
                                        singleLine = true
                                    )
                                },
                                confirmButton = {
                                    TextButton(
                                        onClick = {
                                            if (newName.isNotBlank() && newName != "Temp Current") {
                                                coroutineScope.launch {
                                                    repository.updatePlaylist(playlist!!.copy(name = newName))
                                                }
                                                showSaveDialog = false
                                            }
                                        }
                                    ) { Text("Save") }
                                },
                                dismissButton = {
                                    TextButton(onClick = { showSaveDialog = false }) { Text("Cancel") }
                                }
                            )
                        }
                    }
                }
            )
        },"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "w") as f:
    f.write(content)
