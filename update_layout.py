import re

with open("app/src/main/res/layout/widget_media.xml", "r") as f:
    content = f.read()

# Replace Controls Row
start_tag = "    <!-- Controls Row -->"
end_tag = "    <!-- Playlist / File Explorer Header -->"

if end_tag not in content:
    end_tag = "    <!-- Playlist / File Explorer -->"

start_idx = content.find(start_tag)
end_idx = content.find(end_tag)

if start_idx != -1 and end_idx != -1:
    new_controls = """    <!-- Controls Row 1 (Playback) -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center"
        android:paddingTop="8dp"
        android:paddingBottom="4dp">
        <ImageView
            android:id="@+id/widget_btn_prev"
            android:layout_width="32dp"
            android:layout_height="32dp"
            android:src="@drawable/ic_widget_prev"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_rewind"
            android:layout_width="32dp"
            android:layout_height="32dp"
            android:layout_marginStart="8dp"
            android:src="@drawable/ic_widget_rewind"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_play"
            android:layout_width="40dp"
            android:layout_height="40dp"
            android:layout_marginStart="8dp"
            android:layout_marginEnd="8dp"
            android:src="@drawable/ic_widget_play"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_ffwd"
            android:layout_width="32dp"
            android:layout_height="32dp"
            android:src="@drawable/ic_widget_fastforward"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_next"
            android:layout_width="32dp"
            android:layout_height="32dp"
            android:layout_marginStart="8dp"
            android:src="@drawable/ic_widget_next"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_stop"
            android:layout_width="32dp"
            android:layout_height="32dp"
            android:layout_marginStart="8dp"
            android:src="@drawable/ic_widget_stop"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
    </LinearLayout>

    <!-- Controls Row 2 (Secondary) -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:paddingTop="4dp"
        android:paddingBottom="8dp"
        android:paddingStart="8dp"
        android:paddingEnd="8dp">
        
        <ImageView
            android:id="@+id/widget_btn_shuffle"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:src="@drawable/ic_widget_shuffle"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_loop"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:layout_marginStart="8dp"
            android:src="@drawable/ic_widget_loop"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_refresh"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:layout_marginStart="8dp"
            android:src="@drawable/ic_widget_refresh"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
            
        <FrameLayout
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1" />
            
        <ImageView
            android:id="@+id/widget_btn_search"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:src="@android:drawable/ic_menu_search"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_miniplayer"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:layout_marginStart="8dp"
            android:src="@android:drawable/ic_menu_crop"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_close"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:layout_marginStart="8dp"
            android:src="@android:drawable/ic_menu_close_clear_cancel"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
    </LinearLayout>

    <FrameLayout
        android:layout_width="match_parent"
        android:layout_height="1dp"
        android:background="@drawable/widget_divider_solid" />

"""
    
    explorer_header = """    <!-- Playlist / File Explorer Header -->
    <LinearLayout
        android:id="@+id/widget_explorer_header"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:padding="8dp">
        <ImageView
            android:id="@+id/widget_btn_back"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:src="@drawable/ic_widget_back"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside"
            android:visibility="gone" />
        <TextView
            android:id="@+id/widget_explorer_title"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:layout_marginStart="8dp"
            android:text="Library"
            android:textColor="#19202D"
            android:textSize="14sp"
            android:textStyle="bold" />
    </LinearLayout>

    <FrameLayout
        android:layout_width="match_parent"
        android:layout_height="1dp"
        android:background="@drawable/widget_divider_solid" />

    """

    content = content[:start_idx] + new_controls + explorer_header + content[end_idx + len("    <!-- Playlist / File Explorer Header -->\n") if "Header" in end_tag else end_idx:]
    
    with open("app/src/main/res/layout/widget_media.xml", "w") as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Tags not found")
