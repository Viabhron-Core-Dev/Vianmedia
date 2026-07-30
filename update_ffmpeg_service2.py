import re
with open("app/src/main/java/com/example/service/FFmpegService.kt", "r") as f:
    content = f.read()

target = """            val outStream = getOutputStream(outputUriStr, fileName, getMimeType(outputExt))
            if (outStream != null) {"""
replacement = """            val (finalUri, outStream) = getOutputStreamAndUri(outputUriStr, fileName, getMimeType(outputExt))
            if (outStream != null) {"""
content = content.replace(target, replacement)

target2 = """                    LogKeeper.log("Saved to output folder: $fileName", "FFmpegService")
                } catch (e: Exception) {"""
replacement2 = """                    LogKeeper.log("Saved to output folder: $fileName", "FFmpegService")
                    FFmpegStatus.lastOutputUri = finalUri?.toString()
                } catch (e: Exception) {"""
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/FFmpegService.kt", "w") as f:
    f.write(content)
print("Replaced")
