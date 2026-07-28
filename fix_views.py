with open("app/src/main/res/layout/widget_media.xml", "r") as f:
    content = f.read()

content = content.replace("<View", "<FrameLayout")
content = content.replace("</View>", "</FrameLayout>")

with open("app/src/main/res/layout/widget_media.xml", "w") as f:
    f.write(content)
