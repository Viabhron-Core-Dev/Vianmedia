import re
with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "r") as f:
    content = f.read()

content = content.replace("androidx.media3.session.SessionToken(context,", "androidx.media3.session.SessionToken(context.applicationContext,")
content = content.replace("android.content.ComponentName(context,", "android.content.ComponentName(context.applicationContext,")
content = content.replace("androidx.media3.session.MediaController.Builder(context,", "androidx.media3.session.MediaController.Builder(context.applicationContext,")

with open("app/src/main/java/com/example/widget/MediaWidgetProvider.kt", "w") as f:
    f.write(content)
