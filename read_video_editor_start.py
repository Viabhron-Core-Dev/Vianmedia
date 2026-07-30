with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    lines = f.readlines()
for j in range(150, 180):
    print(f"{j}: {lines[j]}", end="")
