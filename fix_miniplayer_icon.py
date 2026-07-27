with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

target = """            androidx.compose.foundation.Image(
                painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_launcher_foreground),
                contentDescription = "Unfold",
                modifier = Modifier.fillMaxSize()
            )"""

replacement = """            androidx.compose.foundation.Image(
                painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_launcher_foreground),
                contentDescription = "Unfold",
                modifier = Modifier.fillMaxSize(1.6f),
                contentScale = androidx.compose.ui.layout.ContentScale.Crop
            )"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
