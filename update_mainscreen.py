import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

# Replace file system delete block
old_fs_delete = """                                        val imageLoader = context.imageLoader
                                        imageLoader.diskCache?.remove(uri.toString())
                                        imageLoader.memoryCache?.remove(coil.memory.MemoryCache.Key(uri.toString()))
                                    } catch (e: Exception) {"""

new_fs_delete = """                                        val imageLoader = context.imageLoader
                                        imageLoader.diskCache?.remove(uri.toString())
                                        imageLoader.memoryCache?.remove(coil.memory.MemoryCache.Key(uri.toString()))
                                        com.example.data.SettingsManager.getInstance(context).removePlaybackState(uri.toString())
                                    } catch (e: Exception) {"""

content = content.replace(old_fs_delete, new_fs_delete)

# Replace MediaStore delete block
old_ms_delete = """                                        val imageLoader = context.imageLoader
                                        imageLoader.diskCache?.remove(media.uri.toString())
                                        imageLoader.memoryCache?.remove(coil.memory.MemoryCache.Key(media.uri.toString()))
                                    } catch (se: SecurityException) {"""

new_ms_delete = """                                        val imageLoader = context.imageLoader
                                        imageLoader.diskCache?.remove(media.uri.toString())
                                        imageLoader.memoryCache?.remove(coil.memory.MemoryCache.Key(media.uri.toString()))
                                        com.example.data.SettingsManager.getInstance(context).removePlaybackState(media.uri.toString())
                                    } catch (se: SecurityException) {"""

content = content.replace(old_ms_delete, new_ms_delete)

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)

print("Updated MainScreen")
