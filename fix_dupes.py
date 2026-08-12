with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "videoWidth = w" in line and lines[i+1].strip() == "videoHeight = h":
        if "videoWidth = w" in lines[i+2] and lines[i+3].strip() == "videoHeight = h":
            continue # skip the first one
    new_lines.append(line)

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'w') as f:
    f.writelines(new_lines)
