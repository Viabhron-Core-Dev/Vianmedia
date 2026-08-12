import re

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'r') as f:
    content = f.read()

bad_modifier = """        AndroidView(
            modifier = if (resizeMode == 5 && videoWidth > 0 && videoHeight > 0) {
                Modifier.size((videoWidth / density).dp, (videoHeight / density).dp)
            } else {
                Modifier.fillMaxSize()
            },"""
good_modifier = """        AndroidView("""

content = content.replace(bad_modifier, good_modifier)

old_bottom_modifier = """            modifier = Modifier.fillMaxSize().graphicsLayer {"""
new_bottom_modifier = """            modifier = (if (resizeMode == 5 && videoWidth > 0 && videoHeight > 0) Modifier.size((videoWidth / density).dp, (videoHeight / density).dp) else Modifier.fillMaxSize()).graphicsLayer {"""

content = content.replace(old_bottom_modifier, new_bottom_modifier)

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'w') as f:
    f.write(content)
