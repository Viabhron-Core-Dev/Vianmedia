with open("app/src/main/java/com/example/service/FFmpegService.kt", "r") as f:
    content = f.read()

import re

# Find getOutputStreamAndUri and remove the duplicated code below it.
match = re.search(r'private fun getOutputStreamAndUri.*?return Pair\(uri, uri\?\.let \{ contentResolver\.openOutputStream\(it\) \}\)\n    \}', content, re.DOTALL)
if match:
    replacement_str = match.group(0)
    # the rest of the file after this might have the duplicate block
    before = content[:match.end()]
    after = content[match.end():]
    
    # remove the duplicate block in after
    duplicate_match = re.search(r'^\s*\}\n\s*if \(outputUriStr \!= null\).*?return uri\?\.let \{ contentResolver\.openOutputStream\(it\) \}\n    \}', after, re.DOTALL)
    if duplicate_match:
        after = after[:duplicate_match.start()] + after[duplicate_match.end():]
        print("Duplicate block removed")
    
    with open("app/src/main/java/com/example/service/FFmpegService.kt", "w") as f:
        f.write(before + after)

