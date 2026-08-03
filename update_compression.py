import re

with open("app/src/main/java/com/example/ui/components/CompressionOptionsDialog.kt", "r") as f:
    content = f.read()

new_dialog = """package com.example.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp

data class ResolutionOption(val name: String, val width: Int, val height: Int)

val resolutionOptions = listOf(
    ResolutionOption("QQVGA (160x120)", 160, 120),
    ResolutionOption("QVGA (320x240)", 320, 240),
    ResolutionOption("VGA (640x480)", 640, 480),
    ResolutionOption("SVGA (800x600)", 800, 600),
    ResolutionOption("XGA (1024x768)", 1024, 768),
    ResolutionOption("SXGA (1280x1024)", 1280, 1024),
    ResolutionOption("SXGA+ (1400x1050)", 1400, 1050),
    ResolutionOption("UXGA (1600x1200)", 1600, 1200),
    ResolutionOption("QXGA (2048x1536)", 2048, 1536),
    ResolutionOption("Custom size...", -2, -2),
    ResolutionOption("No Resize (Untouched)", -1, -1)
)

@Composable
fun CompressionOptionsDialog(
    uris: List<String>,
    onDismiss: () -> Unit,
    onStartCompression: (uris: List<String>, maxWidth: Int, maxHeight: Int, quality: Int, format: String) -> Unit
) {
    var explicitlyCustom by remember { mutableStateOf(false) }
    var customWidth by remember { mutableStateOf("480") }
    var customHeight by remember { mutableStateOf("360") }
    
    var quality by remember { mutableStateOf(80f) }
    var selectedFormat by remember { mutableStateOf("JPEG") }
    val formats = listOf("JPEG", "PNG", "WEBP")

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Compress Images") },
        text = {
            Column(modifier = Modifier.fillMaxWidth()) {
                Text("Quality: ${quality.toInt()}%", style = MaterialTheme.typography.labelLarge)
                Slider(
                    value = quality,
                    onValueChange = { quality = it },
                    valueRange = 10f..100f,
                    steps = 8
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                Text("Format:", style = MaterialTheme.typography.labelLarge)
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                    formats.forEach { format ->
                        FilterChip(
                            selected = selectedFormat == format,
                            onClick = { selectedFormat = format },
                            label = { Text(format) }
                        )
                    }
                }
                
                Divider(modifier = Modifier.padding(vertical = 8.dp))

                if (explicitlyCustom) {
                    Column {
                        OutlinedTextField(
                            value = customWidth,
                            onValueChange = { customWidth = it },
                            label = { Text("Width") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        OutlinedTextField(
                            value = customHeight,
                            onValueChange = { customHeight = it },
                            label = { Text("Height") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                        )
                    }
                } else {
                    LazyColumn(modifier = Modifier.heightIn(max = 250.dp)) {
                        items(resolutionOptions) { option ->
                            Text(
                                text = option.name,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable {
                                        if (option.width == -2) {
                                            explicitlyCustom = true
                                        } else {
                                            onStartCompression(uris, option.width, option.height, quality.toInt(), selectedFormat)
                                        }
                                    }
                                    .padding(vertical = 12.dp, horizontal = 8.dp),
                                style = MaterialTheme.typography.bodyLarge
                            )
                        }
                    }
                }
            }
        },
        confirmButton = {
            if (explicitlyCustom) {
                TextButton(onClick = {
                    val w = customWidth.toIntOrNull() ?: -1
                    val h = customHeight.toIntOrNull() ?: -1
                    onStartCompression(uris, w, h, quality.toInt(), selectedFormat)
                }) {
                    Text("Compress")
                }
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
"""

with open("app/src/main/java/com/example/ui/components/CompressionOptionsDialog.kt", "w") as f:
    f.write(new_dialog)

with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "r") as f:
    nav_content = f.read()

nav_content = nav_content.replace(
    "onStartCompression = { urisToCompress, w, h ->",
    "onStartCompression = { urisToCompress, w, h, q, f ->"
)

nav_content = nav_content.replace(
    "putExtra(\"maxHeight\", h)\n                    context.startService(this)",
    "putExtra(\"maxHeight\", h)\n                    putExtra(\"quality\", q)\n                    putExtra(\"format\", f)\n                    context.startService(this)"
)

with open("app/src/main/java/com/example/ui/navigation/AppNavigation.kt", "w") as f:
    f.write(nav_content)

with open("app/src/main/java/com/example/BatchActionActivity.kt", "r") as f:
    batch_content = f.read()
    
batch_content = batch_content.replace(
    "onStartCompression = { uris, maxWidth, maxHeight ->",
    "onStartCompression = { uris, maxWidth, maxHeight, quality, format ->"
)

batch_content = batch_content.replace(
    "putExtra(\"maxHeight\", maxHeight)\n                                    }",
    "putExtra(\"maxHeight\", maxHeight)\n                                        putExtra(\"quality\", quality)\n                                        putExtra(\"format\", format)\n                                    }"
)

with open("app/src/main/java/com/example/BatchActionActivity.kt", "w") as f:
    f.write(batch_content)
