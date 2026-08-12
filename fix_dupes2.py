import re

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'r') as f:
    content = f.read()

# Fix the messy block
bad_block = """                PipHelper.updatePipParams(context, controller, w, h)
        videoHeight = h
                videoWidth = w
                videoHeight = h
            }"""
good_block = """                PipHelper.updatePipParams(context, controller, w, h)
                videoWidth = w
                videoHeight = h
            }"""

content = content.replace(bad_block, good_block)

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'w') as f:
    f.write(content)
