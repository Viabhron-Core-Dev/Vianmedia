import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = """                            try {
                                if (!com.facebook.soloader.nativeloader.NativeLoader.isInitialized()) {
                                    com.facebook.soloader.nativeloader.NativeLoader.init(com.facebook.soloader.nativeloader.SystemDelegate())
                                }
                            } catch (e: Exception) {}"""

replacement = """                            try {
                                val clazz = Class.forName("com.facebook.soloader.nativeloader.NativeLoader")
                                val isInitializedMethod = clazz.getMethod("isInitialized")
                                val isInit = isInitializedMethod.invoke(null) as Boolean
                                if (!isInit) {
                                    val delegateClazz = Class.forName("com.facebook.soloader.nativeloader.SystemDelegate")
                                    val delegate = delegateClazz.newInstance()
                                    val delegateInterface = Class.forName("com.facebook.soloader.nativeloader.NativeLoaderDelegate")
                                    val initMethod = clazz.getMethod("init", delegateInterface)
                                    initMethod.invoke(null, delegate)
                                }
                            } catch (e: Exception) {}"""

if target in content:
    content = content.replace(target, replacement)
    print("Success VideoEditorScreen")
else:
    print("Failed VideoEditorScreen")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
