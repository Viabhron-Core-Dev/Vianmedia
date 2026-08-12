import sys

with open('app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt', 'r') as f:
    content = f.read()

target = """                            Text(
                                name, 
                                style = MaterialTheme.typography.bodyMedium, 
                                modifier = Modifier.weight(1f), 
                                maxLines = 2,
                                color = if (isSelected) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                            )"""

replacement = """                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    name, 
                                    style = MaterialTheme.typography.bodyMedium, 
                                    maxLines = 2,
                                    color = if (isSelected) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                if (item.isNotFound) {
                                    Text(
                                        "File not found",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = MaterialTheme.colorScheme.error
                                    )
                                }
                            }"""

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/example/ui/screens/PlaylistDetailScreen.kt', 'w') as f:
        f.write(content)
    print("Updated PlaylistDetailScreen.kt")
else:
    print("Could not update PlaylistDetailScreen.kt")
