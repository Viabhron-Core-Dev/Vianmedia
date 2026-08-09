import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = """    var showExportPanel by remember { mutableStateOf(false) }
    var durationMs by remember { mutableLongStateOf(1L) }
    
    val joinVideoPickerLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.OpenDocument(),
        onResult = { uri ->
            if (uri != null) {
                // Persist permission
                try {
                    context.contentResolver.takePersistableUriPermission(uri, android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                } catch (e: Exception) {}
                editState = editState.copy(joinVideoUri = uri.toString())
            }
        }
    )

    val context = LocalContext.current"""

replacement = """    var showExportPanel by remember { mutableStateOf(false) }
    var durationMs by remember { mutableLongStateOf(1L) }
    
    val context = LocalContext.current
    val joinVideoPickerLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.OpenDocument(),
        onResult = { uri ->
            if (uri != null) {
                // Persist permission
                try {
                    context.contentResolver.takePersistableUriPermission(uri, android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                } catch (e: Exception) {}
                editState = editState.copy(joinVideoUri = uri.toString())
            }
        }
    )"""

if target in content:
    content = content.replace(target, replacement)
    print("Success 1")
else:
    print("Failed 1")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
