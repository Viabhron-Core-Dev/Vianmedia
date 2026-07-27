with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

# 1. Expanded Mini Player container background and border
target_container = """        modifier = Modifier
            .fillMaxSize()
            .clip(RoundedCornerShape(12.dp))
            .background(androidx.compose.ui.graphics.Color.White.copy(alpha = 0.95f))"""

replacement_container = """        modifier = Modifier
            .fillMaxSize()
            .clip(RoundedCornerShape(12.dp))
            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.95f))
            .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.3f), RoundedCornerShape(12.dp))"""
content = content.replace(target_container, replacement_container)

# 2. Top Title Bar background
target_topbar = """            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(androidx.compose.ui.graphics.Color(0xFFF5F5F5))"""

replacement_topbar = """            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.surface)"""
content = content.replace(target_topbar, replacement_topbar)

# 3. Add Divider below the top bar
target_divider = """                    }
                }
            )
            // Controls"""

replacement_divider = """                    }
                }
            )
            HorizontalDivider(color = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f), thickness = 1.dp)
            // Controls"""
content = content.replace(target_divider, replacement_divider)

# 4. Change all 0xFF2196F3 icon tints to onSurface (black in light mode)
# except maybe the progress bar? "header and boundary lines in player should be blue"
# So icons shouldn't be blue. "buttons shouldn't be blue but rather black."
content = content.replace("tint = androidx.compose.ui.graphics.Color(0xFF2196F3)", "tint = MaterialTheme.colorScheme.onSurface")

# Title color in Top bar to onSurface
content = content.replace("color = androidx.compose.ui.graphics.Color.Black", "color = MaterialTheme.colorScheme.onSurface")

# Minimized button background - maybe keep it primaryContainer or surface?
target_minimized_bg = ".background(androidx.compose.ui.graphics.Color(0xFF2196F3))"
replacement_minimized_bg = ".background(MaterialTheme.colorScheme.surface)\n                .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.3f), androidx.compose.foundation.shape.CircleShape)"
content = content.replace(target_minimized_bg, replacement_minimized_bg)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
