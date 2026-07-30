with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if '"Cut"' in line or '"Trim"' in line or 'editState.trimStartMs' in line or 'editState.trimEndMs' in line:
        start = max(0, i - 10)
        end = min(len(lines), i + 20)
        print(f"--- Around line {i} ---")
        for j in range(start, end):
            print(f"{j}: {lines[j]}", end="")
        print("\n")
