import re

with open("app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt", "r") as f:
    content = f.read()

# I will rewrite the LazyColumn itemsIndexed block and the detectDragGestures entirely to make it standard standard!
