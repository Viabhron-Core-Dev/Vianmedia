import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

print("originalH" in content)
print("originalW" in content)
