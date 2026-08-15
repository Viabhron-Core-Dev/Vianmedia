import re

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    content = f.read()

# We will completely rewrite SettingsScreen.kt but keep imports.
# I'll just write a new file content and overwrite it.
