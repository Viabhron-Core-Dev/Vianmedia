import sys

with open('app/src/main/java/com/example/data/BackupManager.kt', 'r') as f:
    content = f.read()

target = """                            val mediaUri = itemJson.getString("media_uri")
                            val itemTimestamp = itemJson.optLong("timestamp", System.currentTimeMillis())

                            dao.insertPlaylistItem(
                                PlaylistItem(
                                    playlistId = playlistId.toInt(),
                                    mediaUri = mediaUri,
                                    timestamp = itemTimestamp
                                )
                            )"""

replacement = """                            val mediaUri = itemJson.getString("media_uri")
                            val itemTimestamp = itemJson.optLong("timestamp", System.currentTimeMillis())

                            var isNotFound = false
                            try {
                                val uri = android.net.Uri.parse(mediaUri)
                                if (uri.scheme == "file") {
                                    isNotFound = !java.io.File(uri.path ?: "").exists()
                                } else if (uri.scheme == "content") {
                                    context.contentResolver.query(uri, null, null, null, null)?.use { cursor ->
                                        if (!cursor.moveToFirst()) isNotFound = true
                                    } ?: run { isNotFound = true }
                                }
                            } catch (e: Exception) {
                                isNotFound = true
                            }

                            dao.insertPlaylistItem(
                                PlaylistItem(
                                    playlistId = playlistId.toInt(),
                                    mediaUri = mediaUri,
                                    timestamp = itemTimestamp,
                                    isNotFound = isNotFound
                                )
                            )"""

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/example/data/BackupManager.kt', 'w') as f:
        f.write(content)
    print("Updated BackupManager.kt")
else:
    print("Could not update BackupManager.kt")

