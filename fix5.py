import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = """                            // For join video, we scale it to match the target or fallback to 1280x720
                            val parts2 = if (res != "Original") res.split("x") else listOf("1280", "720")
                            val fw = parts2[0].toInt()
                            val fh = parts2[1].toInt()
                            
                            val v1 = "[1:v]scale=w=$fw:h=$fh:force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2[v1];"
                            val a1 = "[1:a]anull[a1];"
                            
                            val concat = if (editState.joinAtEnd) {
                                "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"
                            } else {
                                "[v1][a1][v0][a0]concat=n=2:v=1:a=1[v][a]"
                            }
                            
                            val filterComplex = "$v0$a0$v1$a1$concat"
                            // If res is original we still need a common scale to avoid concat errors
                            val v0Safe = if (filterList.isNotEmpty()) {
                                "[0:v]${filterList.joinToString(",")},scale=w=$fw:h=$fh:force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2[v0];"
                            } else {
                                "[0:v]scale=w=$fw:h=$fh:force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2[v0];"
                            }
                            val safeFilterComplex = "$v0Safe$a0$v1$a1$concat"
                            
                            cmd = "-y $trimArgs -i %INPUT% -i '$joinPath' -filter_complex \\"$safeFilterComplex\\" -map \\"[v]\\" -map \\"[a]\\" -r $fps -vcodec libx264 -crf $crf -preset $presetArg %OUTPUT%\""""

replacement = """                            // For join video, we scale it to match the target
                            val fw = globalTargetW
                            val fh = globalTargetH
                            
                            val v1 = "[1:v]scale=w=$fw:h=$fh:force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2,setsar=1[v1];"
                            val a1 = "[1:a]anull[a1];"
                            
                            val concat = if (editState.joinAtEnd) {
                                "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"
                            } else {
                                "[v1][a1][v0][a0]concat=n=2:v=1:a=1[v][a]"
                            }
                            
                            // If res is original we still need a common scale to avoid concat errors
                            val v0Safe = if (filterList.isNotEmpty()) {
                                "[0:v]${filterList.joinToString(",")},scale=w=$fw:h=$fh:force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2,setsar=1[v0];"
                            } else {
                                "[0:v]scale=w=$fw:h=$fh:force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2,setsar=1[v0];"
                            }
                            val safeFilterComplex = "$v0Safe$a0$v1$a1$concat"
                            
                            cmd = "-y $trimArgs -i %INPUT% -i '$joinPath' -filter_complex \\"$safeFilterComplex\\" -map \\"[v]\\" -map \\"[a]\\" -r $fps -vcodec libx264 -crf $crf -preset $presetArg %OUTPUT%\""""

if target in content:
    content = content.replace(target, replacement)
    print("Success 1")
else:
    print("Failed 1")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
