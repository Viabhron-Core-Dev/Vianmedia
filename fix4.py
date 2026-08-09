import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = """                        if (res != "Original") {
                            val parts = res.split("x")
                            var targetW = parts[0].toInt()
                            var targetH = parts[1].toInt()
                            
                            val originalW = videoWidth
                            val originalH = videoHeight
                            val rotatedW = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) originalH else originalW
                            val rotatedH = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) originalW else originalH
                            
                            val isPortrait = when (exportOrientation) {
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
                            
                            if (isPortrait) {
                                val temp = targetW
                                targetW = targetH
                                targetH = temp
                            }
                            
                            filterList.add("scale=w=$targetW:h=$targetH:force_original_aspect_ratio=decrease:flags=lanczos")
                        }"""

replacement = """                        if (res != "Original") {
                            filterList.add("scale=w=$globalTargetW:h=$globalTargetH:force_original_aspect_ratio=decrease:flags=lanczos")
                        }"""

if target in content:
    content = content.replace(target, replacement)
    print("Success 1")
else:
    print("Failed 1")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
