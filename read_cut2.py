with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'Row(modifier = Modifier.padding(top = 8.dp)) {' in line:
        start = max(0, i - 15)
        end = min(len(lines), i + 10)
        print(f"--- Around line {i} ---")
        for j in range(start, end):
            print(f"{j}: {lines[j]}", end="")
        print("\n")
        break
