import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

old_res_block = """                        if (res != "Original") {
                            val parts = res.split("x")
                            var targetW = parts[0].toInt()
                            var targetH = parts[1].toInt()
                            
                            val isOriginalPortrait = (exoPlayer?.videoSize?.height ?: 0) > (exoPlayer?.videoSize?.width ?: 1)
                            val rotatedPortrait = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) !isOriginalPortrait else isOriginalPortrait
                            
                            if (rotatedPortrait) {
                                val temp = targetW
                                targetW = targetH
                                targetH = temp
                            }
                            
                            filterList.add("scale=w=$targetW:h=$targetH:force_original_aspect_ratio=decrease:flags=lanczos,pad=$targetW:$targetH:(ow-iw)/2:(oh-ih)/2")
                        }
                        
                        val videoFilterArgs = if (filterList.isNotEmpty()) {"""

new_res_block = """                        if (res != "Original") {
                            val parts = res.split("x")
                            var targetW = parts[0].toInt()
                            var targetH = parts[1].toInt()
                            
                            val originalW = exoPlayer?.videoSize?.width ?: 1
                            val originalH = exoPlayer?.videoSize?.height ?: 1
                            val rotatedW = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) originalH else originalW
                            val rotatedH = if (editState.rotateConfig == 90 || editState.rotateConfig == 270) originalW else originalH
                            
                            val isPortrait = when {
                                editState.aspectRatio == "9:16" -> true
                                editState.aspectRatio == "16:9" -> false
                                editState.aspectRatio == "4:3" -> false
                                editState.aspectRatio == "21:9" -> false
                                editState.aspectRatio == "1:1" -> false
                                editState.cropRect == "Custom" -> {
                                    val cw = rotatedW * (editState.cropRight - editState.cropLeft)
                                    val ch = rotatedH * (editState.cropBottom - editState.cropTop)
                                    ch > cw
                                }
                                editState.cropRect == "Center Crop" -> false
                                else -> rotatedH > rotatedW
                            }
                            
                            if (isPortrait) {
                                val temp = targetW
                                targetW = targetH
                                targetH = temp
                            }
                            
                            filterList.add("scale=w=$targetW:h=$targetH:force_original_aspect_ratio=decrease:flags=lanczos")
                        }
                        
                        // Always ensure even dimensions for libx264 compatibility
                        filterList.add("scale=trunc(iw/2)*2:trunc(ih/2)*2")
                        
                        val videoFilterArgs = if (filterList.isNotEmpty()) {"""

if old_res_block in content:
    content = content.replace(old_res_block, new_res_block)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Fixed resolution and cropping math!")
else:
    print("Could not find res block")
