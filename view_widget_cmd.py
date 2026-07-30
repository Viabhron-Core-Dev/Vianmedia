with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "widgetCommandReceiver" in line or "ACTION_WIDGET_COMMAND" in line:
        start = max(0, i-2)
        for j in range(start, min(len(lines), start+20)):
            print(lines[j], end='')
        break
