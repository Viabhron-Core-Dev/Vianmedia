import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = """                        var joinPath: String? = null
                        if (editState.joinVideoUri != null) {
                            try {
                                val u = android.net.Uri.parse(editState.joinVideoUri!!)
                                val tempFile = java.io.File(context.cacheDir, "join_${System.currentTimeMillis()}.mp4")
                                context.contentResolver.openInputStream(u)?.use { input ->
                                    tempFile.outputStream().use { output ->
                                        input.copyTo(output)
                                    }
                                }
                                joinPath = tempFile.absolutePath
                            } catch (e: Exception) {
                                e.printStackTrace()
                            }
                        }
                        
                        // 2. Build FFmpeg command template based on edits
                        val filterList = mutableListOf<String>()"""

replacement = """                        var joinPath: String? = null
                        if (editState.joinVideoUri != null) {
                            try {
                                val u = android.net.Uri.parse(editState.joinVideoUri!!)
                                val tempFile = java.io.File(context.cacheDir, "join_${System.currentTimeMillis()}.mp4")
                                context.contentResolver.openInputStream(u)?.use { input ->
                                    tempFile.outputStream().use { output ->
                                        input.copyTo(output)
                                    }
                                }
                                joinPath = tempFile.absolutePath
                            } catch (e: Exception) {
                                e.printStackTrace()
                            }
                        }
                        
                        val originalW = videoWidth
                        val originalH = videoHeight
                        val rotatedW = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) originalH else originalW
                        val rotatedH = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) originalW else originalH
                        
                        val isPortraitFinal = when (exportOrientation) {
                            "Portrait" -> true
                            "Landscape" -> false
                            else -> when {
                                editState.aspectRatio == "9:16" -> true
                                editState.aspectRatio == "16:9" -> false
                                editState.aspectRatio == "4:3" -> false
                                editState.aspectRatio == "21:9" -> false
                                editState.aspectRatio == "1:1" -> false
                                editState.cropRect == "9:16" -> true
                                editState.cropRect == "16:9" -> false
                                editState.cropRect == "Fill 16:9" -> false
                                editState.cropRect == "4:3" -> false
                                editState.cropRect == "21:9" -> false
                                editState.cropRect == "1:1" -> false
                                editState.cropRect == "Custom" -> {
                                    val cw = rotatedW * (editState.cropRight - editState.cropLeft)
                                    val ch = rotatedH * (editState.cropBottom - editState.cropTop)
                                    ch > cw
                                }
                                editState.cropRect == "Center Crop" -> false
                                else -> rotatedH > rotatedW
                            }
                        }
                        
                        var globalTargetW = 1280
                        var globalTargetH = 720
                        if (res != "Original") {
                            val parts = res.split("x")
                            globalTargetW = parts[0].toInt()
                            globalTargetH = parts[1].toInt()
                        } else {
                            globalTargetW = if (isPortraitFinal) 720 else 1280
                            globalTargetH = if (isPortraitFinal) 1280 else 720
                        }
                        if (isPortraitFinal && res != "Original") {
                            val temp = globalTargetW
                            globalTargetW = globalTargetH
                            globalTargetH = temp
                        }

                        // 2. Build FFmpeg command template based on edits
                        val filterList = mutableListOf<String>()"""

if target in content:
    content = content.replace(target, replacement)
    print("Success 1")
else:
    print("Failed 1")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
