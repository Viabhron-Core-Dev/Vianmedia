import sys, re

with open('app/src/main/java/com/example/ui/screens/PlayerSettingsScreen.kt', 'r') as f:
    content = f.read()

replacement = """            }
            
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "Keep Screen Awake",
                        style = MaterialTheme.typography.titleMedium
                    )
                    Text(
                        text = "Keep screen on while video is playing",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Switch(
                    checked = keepScreenAwake,
                    onCheckedChange = { 
                        settingsManager.setKeepScreenAwake(it)
                    }
                )
            }
            
            var decoderPriority"""

content = re.sub(r'            \}\s*var decoderPriority', replacement, content)

with open('app/src/main/java/com/example/ui/screens/PlayerSettingsScreen.kt', 'w') as f:
    f.write(content)
print("Done")
