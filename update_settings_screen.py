import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

var_old = """    var showPlayerSettingsDialog by remember { mutableStateOf(false) }"""
var_new = """    var showPlayerSettingsDialog by remember { mutableStateOf(false) }
    var showAudioSettingsDialog by remember { mutableStateOf(false) }"""

content = content.replace(var_old, var_new)

nav_old = """            Text("Player Settings", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(8.dp))
            Button(onClick = { showPlayerSettingsDialog = true }) {
                Text("Open Player Settings")
            }"""

nav_new = """            Text("Player Settings", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(8.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(onClick = { showPlayerSettingsDialog = true }, modifier = Modifier.weight(1f)) {
                    Text("Player Settings")
                }
                FilledTonalButton(onClick = { showAudioSettingsDialog = true }, modifier = Modifier.weight(1f)) {
                    Text("Audio & EQ")
                }
            }"""

content = content.replace(nav_old, nav_new)

dialog_old = """            if (showPlayerSettingsDialog) {
                androidx.compose.ui.window.Dialog(
                    onDismissRequest = { showPlayerSettingsDialog = false },
                    properties = androidx.compose.ui.window.DialogProperties(usePlatformDefaultWidth = false)
                ) {
                    PlayerSettingsScreen(onNavigateBack = { showPlayerSettingsDialog = false })
                }
            }"""
            
dialog_new = """            if (showPlayerSettingsDialog) {
                androidx.compose.ui.window.Dialog(
                    onDismissRequest = { showPlayerSettingsDialog = false },
                    properties = androidx.compose.ui.window.DialogProperties(usePlatformDefaultWidth = false)
                ) {
                    PlayerSettingsScreen(onNavigateBack = { showPlayerSettingsDialog = false })
                }
            }
            
            if (showAudioSettingsDialog) {
                androidx.compose.ui.window.Dialog(
                    onDismissRequest = { showAudioSettingsDialog = false },
                    properties = androidx.compose.ui.window.DialogProperties(usePlatformDefaultWidth = false)
                ) {
                    AudioSettingsScreen(onNavigateBack = { showAudioSettingsDialog = false })
                }
            }"""

content = content.replace(dialog_old, dialog_new)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
