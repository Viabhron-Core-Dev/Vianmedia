import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = """    setContent {
      val currentIntent by _currentIntent.collectAsState()
      val settings = com.example.data.SettingsManager.getInstance(this)
      com.example.service.PlayerManager.initialize(this, false)
      MyApplicationTheme {"""

replacement = """    setContent {
      val currentIntent by _currentIntent.collectAsState()
      val settings = com.example.data.SettingsManager.getInstance(this)
      val themePref by settings.themePreference.collectAsState()
      val fontPref by settings.fontPreference.collectAsState()
      com.example.service.PlayerManager.initialize(this, false)
      MyApplicationTheme(themePreference = themePref, fontPreference = fontPref) {"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
