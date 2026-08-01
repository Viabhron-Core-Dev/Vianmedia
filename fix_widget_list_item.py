import re
with open("app/src/main/res/layout/widget_list_item.xml", "r") as f:
    content = f.read()

# Modify root padding
content = re.sub(r'android:padding="8dp"', 'android:paddingStart="16dp"\n    android:paddingEnd="16dp"\n    android:paddingTop="12dp"\n    android:paddingBottom="12dp"', content)

# Modify icon size and margin
content = re.sub(r'android:layout_width="20dp"', 'android:layout_width="24dp"', content)
content = re.sub(r'android:layout_height="20dp"', 'android:layout_height="24dp"', content)
content = re.sub(r'android:layout_marginEnd="8dp"', 'android:layout_marginEnd="16dp"', content)

# Modify text size
content = re.sub(r'android:textSize="12sp"', 'android:textSize="14sp"', content)

with open("app/src/main/res/layout/widget_list_item.xml", "w") as f:
    f.write(content)
print("Adjusted widget list item")
