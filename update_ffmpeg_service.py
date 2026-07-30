with open("app/src/main/java/com/example/service/FFmpegService.kt", "r") as f:
    content = f.read()

target1 = """    private fun getOutputStream(outputUriStr: String?, fileName: String, mimeType: String): java.io.OutputStream? {"""
replacement1 = """    private fun getOutputStreamAndUri(outputUriStr: String?, fileName: String, mimeType: String): Pair<Uri?, java.io.OutputStream?> {
        if (outputUriStr != null) {
            try {
                val treeUri = Uri.parse(outputUriStr)
                val docId = android.provider.DocumentsContract.getTreeDocumentId(treeUri)
                val docUri = android.provider.DocumentsContract.buildDocumentUriUsingTree(treeUri, docId)
                val newUri = android.provider.DocumentsContract.createDocument(
                    contentResolver,
                    docUri,
                    mimeType,
                    fileName
                )
                if (newUri != null) {
                    return Pair(newUri, contentResolver.openOutputStream(newUri))
                }
            } catch (e: Exception) {
                LogKeeper.logError("FFmpegService", "Failed SAF create", e)
            }
        }
        // Fallback to media store
        val contentValues = android.content.ContentValues().apply {
            put(android.provider.MediaStore.MediaColumns.DISPLAY_NAME, fileName)
            put(android.provider.MediaStore.MediaColumns.MIME_TYPE, mimeType)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                val relativePath = if (mimeType.startsWith("audio")) android.os.Environment.DIRECTORY_MUSIC else android.os.Environment.DIRECTORY_MOVIES
                put(android.provider.MediaStore.MediaColumns.RELATIVE_PATH, "$relativePath/Edited")
            }
        }
        val collection = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            if (mimeType.startsWith("audio")) android.provider.MediaStore.Audio.Media.EXTERNAL_CONTENT_URI else android.provider.MediaStore.Video.Media.EXTERNAL_CONTENT_URI
        } else {
            if (mimeType.startsWith("audio")) android.provider.MediaStore.Audio.Media.EXTERNAL_CONTENT_URI else android.provider.MediaStore.Video.Media.EXTERNAL_CONTENT_URI
        }
        val uri = contentResolver.insert(collection, contentValues)
        return Pair(uri, uri?.let { contentResolver.openOutputStream(it) })
    }
"""

target2 = """                try {
                    getOutputStream(outputUriStr, fileName, mimeType)?.use { outputStream ->"""
replacement2 = """                try {
                    val (finalUri, outputStream) = getOutputStreamAndUri(outputUriStr, fileName, mimeType)
                    outputStream?.use { outStream ->"""

content = content.replace(target1, replacement1)
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/FFmpegService.kt", "w") as f:
    f.write(content)
print("Replaced")
