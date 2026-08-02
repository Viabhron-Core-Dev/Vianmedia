import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

old_launcher = """    val deleteLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.StartIntentSenderForResult()
    ) { result ->
        if (result.resultCode == android.app.Activity.RESULT_OK) {
            selectedFolderId?.let { viewModel.scanFolder(it) } ?: viewModel.loadMedia()
            selectedMediaItems.clear()
            showDeleteConfirmDialog = false
        }
    }"""

new_launcher = """    val deleteLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.StartIntentSenderForResult()
    ) { result ->
        if (result.resultCode == android.app.Activity.RESULT_OK) {
            val imageLoader = context.imageLoader
            val settings = com.example.data.SettingsManager.getInstance(context)
            selectedMediaItems.forEach { media ->
                val uriStr = media.uri.toString()
                imageLoader.diskCache?.remove(uriStr)
                imageLoader.memoryCache?.remove(coil.memory.MemoryCache.Key(uriStr))
                settings.removePlaybackState(uriStr)
            }
            selectedFolderId?.let { viewModel.scanFolder(it) } ?: viewModel.loadMedia()
            selectedMediaItems.clear()
            showDeleteConfirmDialog = false
        }
    }"""

content = content.replace(old_launcher, new_launcher)

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)
