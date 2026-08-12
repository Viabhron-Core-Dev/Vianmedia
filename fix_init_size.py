import re

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'r') as f:
    content = f.read()

size_change = r"PipHelper\.updatePipParams\(context, controller, w, h\)\n           \n        val pipReceiver ="
new_size_change = """PipHelper.updatePipParams(context, controller, w, h)
        videoWidth = w
        videoHeight = h
           
        val pipReceiver ="""
content = re.sub(size_change, new_size_change, content)

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'w') as f:
    f.write(content)
