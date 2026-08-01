import re

with open("app/src/main/res/layout/widget_media.xml", "r") as f:
    content = f.read()

# I will just find the second occurrence of the block
idx1 = content.find('<LinearLayout\n        android:id="@+id/widget_explorer_header"')
idx2 = content.find('<LinearLayout\n        android:id="@+id/widget_explorer_header"', idx1 + 10)

if idx2 != -1:
    end_idx = content.find('</LinearLayout>', idx2) + 15
    next_frame_end = content.find('/>', end_idx) + 2
    
    content = content[:idx2] + content[next_frame_end:]
    
    with open("app/src/main/res/layout/widget_media.xml", "w") as f:
        f.write(content)
    print("Fixed duplicates again")

