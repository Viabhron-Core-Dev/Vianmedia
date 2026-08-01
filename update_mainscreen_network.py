import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

# 1. Add var showNetworkStreamDialog
var_settings_dialog = "var showSettingsDialog by rememberSaveable { mutableStateOf(false) }"
new_var_network_dialog = "var showSettingsDialog by rememberSaveable { mutableStateOf(false) }\n    var showNetworkStreamDialog by rememberSaveable { mutableStateOf(false) }"
content = content.replace(var_settings_dialog, new_var_network_dialog)

# 2. Add DropdownMenuItem
sort_by_date_menu = """DropdownMenuItem(text = { Text("Sort by Date") }, onClick = { sortOrder = SortOrder.DATE; showOverflowMenu = false })"""
network_stream_menu = sort_by_date_menu + """\n                                DropdownMenuItem(text = { Text("Network Stream") }, onClick = { showNetworkStreamDialog = true; showOverflowMenu = false })"""
content = content.replace(sort_by_date_menu, network_stream_menu)

# 3. Add AlertDialog before if (showSettingsDialog)
settings_dialog_block = "if (showSettingsDialog) {"
network_dialog_code = """
    if (showNetworkStreamDialog) {
        var streamUrl by rememberSaveable { mutableStateOf("") }
        androidx.compose.material3.AlertDialog(
            onDismissRequest = { showNetworkStreamDialog = false },
            title = { Text("Network Stream") },
            text = {
                OutlinedTextField(
                    value = streamUrl,
                    onValueChange = { streamUrl = it },
                    label = { Text("Stream URL") },
                    placeholder = { Text("http://..., rtsp://...") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        if (streamUrl.isNotBlank()) {
                            onNavigateToPlayer(streamUrl)
                            showNetworkStreamDialog = false
                        }
                    }
                ) {
                    Text("Play")
                }
            },
            dismissButton = {
                TextButton(onClick = { showNetworkStreamDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    if (showSettingsDialog) {"""
content = content.replace(settings_dialog_block, network_dialog_code.strip())

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)

print("Updated MainScreen.kt")
