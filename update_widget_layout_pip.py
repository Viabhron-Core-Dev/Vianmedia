with open("app/src/main/res/layout/widget_media.xml", "r") as f:
    content = f.read()

new_btn_pip = """        <ImageView
            android:id="@+id/widget_btn_pip"
            android:layout_width="32dp"
            android:layout_height="32dp"
            android:src="@drawable/ic_pip"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside"
            android:layout_marginStart="8dp" />

        <ImageView
            android:id="@+id/widget_btn_open_app" """

content = content.replace('        <ImageView\n            android:id="@+id/widget_btn_open_app" ', new_btn_pip)

with open("app/src/main/res/layout/widget_media.xml", "w") as f:
    f.write(content)
