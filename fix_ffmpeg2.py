import re
with open("app/src/main/java/com/example/service/FFmpegService.kt", "r") as f:
    content = f.read()

target = """    }
        if (outputUriStr != null) {"""

# Replace from `        if (outputUriStr != null) {` down to `return uri?.let { contentResolver.openOutputStream(it) }`

match = re.search(r'        if \(outputUriStr \!= null\).*?return uri\?\.let \{ contentResolver\.openOutputStream\(it\) \}\n    \}', content, re.DOTALL)
if match:
    content = content[:match.start()] + content[match.end():]
    with open("app/src/main/java/com/example/service/FFmpegService.kt", "w") as f:
        f.write(content)
    print("Fixed.")
else:
    print("Not found.")
