with open("app/src/main/res/layout/widget_media.xml", "r") as f:
    content = f.read()

content = content.replace("<Space", "<FrameLayout")
content = content.replace("</Space>", "</FrameLayout>")

with open("app/src/main/res/layout/widget_media.xml", "w") as f:
    f.write(content)
print("Replaced")
