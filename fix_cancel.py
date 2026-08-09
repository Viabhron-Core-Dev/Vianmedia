import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = """                        } catch (e: Exception) {
                            LogKeeper.logError("VideoEditor", "Frame extraction failed: ${e.message}", e)
                        }"""

replacement = """                        } catch (e: kotlinx.coroutines.CancellationException) {
                            throw e
                        } catch (e: Exception) {
                            LogKeeper.logError("VideoEditor", "Frame extraction failed: ${e.message}", e)
                        }"""

if target in content:
    content = content.replace(target, replacement)
    print("Success cancel 1")
else:
    print("Failed cancel 1")

target2 = """            } catch (e: Exception) {
                LogKeeper.logError("VideoEditor", "Pre-conversion failed: ${e.message}", e)
            }
            isConverting = false"""

replacement2 = """            } catch (e: kotlinx.coroutines.CancellationException) {
                throw e
            } catch (e: Exception) {
                LogKeeper.logError("VideoEditor", "Pre-conversion failed: ${e.message}", e)
            }
            isConverting = false"""

if target2 in content:
    content = content.replace(target2, replacement2)
    print("Success cancel 2")
else:
    print("Failed cancel 2")

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
