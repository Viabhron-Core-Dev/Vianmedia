import re

with open('app/src/main/java/com/example/data/SettingsManager.kt', 'r') as f:
    content = f.read()

props = """    private val _keepScreenAwake = MutableStateFlow(true)
    val keepScreenAwake: StateFlow<Boolean> = _keepScreenAwake.asStateFlow()

    private val _themePreference = MutableStateFlow("System Default")
    val themePreference: StateFlow<String> = _themePreference.asStateFlow()

    private val _fontPreference = MutableStateFlow("Default")
    val fontPreference: StateFlow<String> = _fontPreference.asStateFlow()"""

content = content.replace("    private val _keepScreenAwake = MutableStateFlow(true)\n    val keepScreenAwake: StateFlow<Boolean> = _keepScreenAwake.asStateFlow()", props)

init_vals = """        _showLoggerFab.value = prefs.getBoolean("show_logger_fab", true)
        _keepScreenAwake.value = prefs.getBoolean("keep_screen_awake", true)

        _themePreference.value = prefs.getString("theme_preference", "System Default") ?: "System Default"
        _fontPreference.value = prefs.getString("font_preference", "Default") ?: "Default"
"""

content = content.replace("        _showLoggerFab.value = prefs.getBoolean(\"show_logger_fab\", true)\n        _keepScreenAwake.value = prefs.getBoolean(\"keep_screen_awake\", true)", init_vals)

setters = """    fun setKeepScreenAwake(keep: Boolean) {
        _keepScreenAwake.value = keep
        prefs.edit().putBoolean("keep_screen_awake", keep).apply()
    }

    fun setThemePreference(theme: String) {
        _themePreference.value = theme
        prefs.edit().putString("theme_preference", theme).apply()
    }

    fun setFontPreference(font: String) {
        _fontPreference.value = font
        prefs.edit().putString("font_preference", font).apply()
    }"""

content = content.replace("    fun setKeepScreenAwake(keep: Boolean) {\n        _keepScreenAwake.value = keep\n        prefs.edit().putBoolean(\"keep_screen_awake\", keep).apply()\n    }", setters)

with open('app/src/main/java/com/example/data/SettingsManager.kt', 'w') as f:
    f.write(content)
