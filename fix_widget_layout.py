import re

with open("app/src/main/res/layout/widget_media.xml", "r") as f:
    content = f.read()

# Replace top bar
top_bar_old = """    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:background="@drawable/widget_topbar_bg"
        android:padding="8dp">
        <TextView
            android:id="@+id/widget_title"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="No Media"
            android:textColor="#19202D"
            android:textSize="14sp"
            android:maxLines="1"
            android:ellipsize="end"
            android:textStyle="bold" />
        <ImageView
            android:id="@+id/widget_btn_refresh"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:layout_marginStart="8dp"
            android:src="@android:drawable/ic_popup_sync"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_pip"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:layout_marginStart="8dp"
            android:src="@android:drawable/ic_menu_gallery"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_expand"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:layout_marginStart="8dp"
            android:src="@android:drawable/ic_menu_view"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
    </LinearLayout>"""

top_bar_new = """    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:background="@drawable/widget_topbar_bg"
        android:padding="8dp">
        <TextView
            android:id="@+id/widget_title"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="No Media"
            android:textColor="#19202D"
            android:textSize="14sp"
            android:maxLines="1"
            android:ellipsize="end"
            android:textStyle="bold" />
        <ImageView
            android:id="@+id/widget_btn_pip"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:layout_marginStart="8dp"
            android:src="@android:drawable/ic_menu_gallery"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
        <ImageView
            android:id="@+id/widget_btn_expand"
            android:layout_width="28dp"
            android:layout_height="28dp"
            android:layout_marginStart="8dp"
            android:src="@android:drawable/ic_menu_view"
            android:background="@drawable/widget_btn_bg"
            android:scaleType="centerInside" />
    </LinearLayout>"""

content = content.replace(top_bar_old, top_bar_new)

# Replace Controls Row
controls_old = """    <!-- Controls Row -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:padding="8dp">
        
        <!-- Playback Controls -->
        <LinearLayout
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center_vertical">
            <ImageView
                android:id="@+id/widget_btn_prev"
                android:layout_width="32dp"
                android:layout_height="32dp"
                android:src="@drawable/ic_widget_prev"
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
                android:id="@+id/widget_btn_next"
                android:layout_width="32dp"
                android:layout_height="32dp"
                android:src="@drawable/ic_widget_next"
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
                android:id="@+id/widget_btn_shuffle"
                android:layout_width="28dp"
                android:layout_height="28dp"
                android:layout_marginStart="4dp"
                android:src="@drawable/ic_widget_shuffle"
                android:background="@drawable/widget_btn_bg"
                android:scaleType="centerInside" />
        </LinearLayout>
        
        <FrameLayout
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1" />
            
        <!-- Bottom right corner buttons: Close/Stop, Search, Open Mini Player -->
        <LinearLayout
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center_vertical">
            
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
    </LinearLayout>"""

controls_new = """    <!-- Controls Row 1 (Playback) -->
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
    </LinearLayout>"""

content = content.replace(controls_old, controls_new)

# Add Explorer Header
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

content = content.replace("    <!-- Playlist / File Explorer -->", explorer_header + "    <!-- Playlist / File Explorer -->")

with open("app/src/main/res/layout/widget_media.xml", "w") as f:
    f.write(content)
print("Updated widget layout")
