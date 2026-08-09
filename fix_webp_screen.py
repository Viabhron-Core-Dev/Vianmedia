import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = """                            val bytes = inputFile.readBytes()
                            val webpImage = com.facebook.animated.webp.WebPImage.createFromByteArray(bytes, com.facebook.imagepipeline.common.ImageDecodeOptions.defaults())"""

replacement = """                            val bytes = inputFile.readBytes()
                            try {
                                if (!com.facebook.soloader.nativeloader.NativeLoader.isInitialized()) {
                                    com.facebook.soloader.nativeloader.NativeLoader.init(com.facebook.soloader.nativeloader.SystemDelegate())
                                }
                            } catch (e: Exception) {}
                            val webpImage = com.facebook.animated.webp.WebPImage.createFromByteArray(bytes, com.facebook.imagepipeline.common.ImageDecodeOptions.defaults())"""

if target in content:
    content = content.replace(target, replacement)
    print("Success VideoEditorScreen")
else:
    print("Failed VideoEditorScreen")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
