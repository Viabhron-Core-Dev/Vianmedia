with open("app/src/main/java/com/example/service/PlaybackService.kt", "r") as f:
    lines = f.readlines()
for i, line in enumerate(lines[426:450]):
    print(line, end='')
