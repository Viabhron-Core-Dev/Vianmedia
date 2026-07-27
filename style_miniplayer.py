with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "r") as f:
    content = f.read()

# Replace the folded mini player button sizes
content = content.replace(".size(48.dp)", ".size(40.dp)")
content = content.replace("modifier = Modifier.size(24.dp)", "modifier = Modifier.size(20.dp)")

# Replace the expanded mini player background color
target_expanded_bg = ".background(androidx.compose.ui.graphics.Color(0xFF2196F3).copy(alpha = 0.95f))"
replacement_expanded_bg = ".background(androidx.compose.ui.graphics.Color.White.copy(alpha = 0.95f))"
content = content.replace(target_expanded_bg, replacement_expanded_bg)

# Replace the top title bar background and drag handle color
target_topbar_bg = ".background(androidx.compose.ui.graphics.Color(0xFF1976D2))"
replacement_topbar_bg = ".background(androidx.compose.ui.graphics.Color(0xFFF5F5F5))"
content = content.replace(target_topbar_bg, replacement_topbar_bg)

target_draghandle = "Icon(Icons.Filled.DragHandle, contentDescription = \"Drag to move\", tint = androidx.compose.ui.graphics.Color.White)"
replacement_draghandle = "Icon(Icons.Filled.DragHandle, contentDescription = \"Drag to move\", tint = androidx.compose.ui.graphics.Color(0xFF2196F3))"
content = content.replace(target_draghandle, replacement_draghandle)

# Title text color
target_title = """                    text = title,
                    style = MaterialTheme.typography.labelMedium,
                    color = androidx.compose.ui.graphics.Color.White,"""
replacement_title = """                    text = title,
                    style = MaterialTheme.typography.labelMedium,
                    color = androidx.compose.ui.graphics.Color.Black,"""
content = content.replace(target_title, replacement_title)

# PIP and Fold icons in the top bar
target_pip_icon = "Icon(androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_picture_in_picture), contentDescription = \"PIP\", tint = androidx.compose.ui.graphics.Color.White, modifier = Modifier.size(16.dp))"
replacement_pip_icon = "Icon(androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_picture_in_picture), contentDescription = \"PIP\", tint = androidx.compose.ui.graphics.Color(0xFF2196F3), modifier = Modifier.size(16.dp))"
content = content.replace(target_pip_icon, replacement_pip_icon)

target_fold_icon = "Icon(androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_close_fullscreen), contentDescription = \"Fold\", tint = androidx.compose.ui.graphics.Color.White, modifier = Modifier.size(16.dp))"
replacement_fold_icon = "Icon(androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_close_fullscreen), contentDescription = \"Fold\", tint = androidx.compose.ui.graphics.Color(0xFF2196F3), modifier = Modifier.size(16.dp))"
content = content.replace(target_fold_icon, replacement_fold_icon)

# Close icon
target_close_icon = "Icon(Icons.Filled.Close, contentDescription = \"Close\", tint = androidx.compose.ui.graphics.Color.White, modifier = Modifier.size(24.dp))"
replacement_close_icon = "Icon(Icons.Filled.Close, contentDescription = \"Close\", tint = androidx.compose.ui.graphics.Color(0xFF2196F3), modifier = Modifier.size(24.dp))"
content = content.replace(target_close_icon, replacement_close_icon)

# Progress bar
target_thumb = """                        Box(
                            modifier = Modifier
                                .size(12.dp)
                                .background(androidx.compose.ui.graphics.Color.White, androidx.compose.foundation.shape.CircleShape)
                        )"""
replacement_thumb = """                        Box(
                            modifier = Modifier
                                .size(12.dp)
                                .background(androidx.compose.ui.graphics.Color(0xFF2196F3), androidx.compose.foundation.shape.CircleShape)
                        )"""
content = content.replace(target_thumb, replacement_thumb)

target_track = """                            colors = SliderDefaults.colors(
                                activeTrackColor = androidx.compose.ui.graphics.Color.White,
                                inactiveTrackColor = androidx.compose.ui.graphics.Color.White.copy(alpha = 0.3f)
                            ),"""
replacement_track = """                            colors = SliderDefaults.colors(
                                activeTrackColor = androidx.compose.ui.graphics.Color(0xFF2196F3),
                                inactiveTrackColor = androidx.compose.ui.graphics.Color.LightGray
                            ),"""
content = content.replace(target_track, replacement_track)

# Playback controls
target_controls_tint = "tint = androidx.compose.ui.graphics.Color.White"
replacement_controls_tint = "tint = androidx.compose.ui.graphics.Color(0xFF2196F3)"
content = content.replace(target_controls_tint, replacement_controls_tint)

with open("app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt", "w") as f:
    f.write(content)
