import re

with open("app/src/main/res/layout/widget_media.xml", "r") as f:
    content = f.read()

# I accidentally duplicated the explorer header. Let's fix that.
dup = """    <!-- Playlist / File Explorer Header -->
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
        android:background="@drawable/widget_divider_solid" />"""

single = """    <!-- Playlist / File Explorer Header -->
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
        android:background="@drawable/widget_divider_solid" />"""

if dup in content:
    content = content.replace(dup, single)
else:
    # Just do a regex to replace any consecutive identical LinearLayouts with that ID
    pass

with open("app/src/main/res/layout/widget_media.xml", "w") as f:
    f.write(content)
print("Duplicate fixed")
