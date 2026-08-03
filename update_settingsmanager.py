import re

with open("app/src/main/java/com/example/data/SettingsManager.kt", "r") as f:
    content = f.read()

new_props = """
    var centerChannelEnabled: Boolean
        get() = prefs.getBoolean("center_channel_enabled", false)
        set(value) {
            prefs.edit().putBoolean("center_channel_enabled", value).apply()
            com.example.service.PlayerManager.applyAudioEffects(this)
        }

    var eqEnabled: Boolean
        get() = prefs.getBoolean("eq_enabled", false)
        set(value) {
            prefs.edit().putBoolean("eq_enabled", value).apply()
            com.example.service.PlayerManager.applyAudioEffects(this)
        }

    var nightModeEnabled: Boolean
        get() = prefs.getBoolean("night_mode_enabled", false)
        set(value) {
            prefs.edit().putBoolean("night_mode_enabled", value).apply()
            com.example.service.PlayerManager.applyAudioEffects(this)
        }
        
    fun getEqLevels(): List<Int> {
        val str = prefs.getString("eq_levels", "") ?: ""
        if (str.isEmpty()) return emptyList()
        return try {
            str.split(",").map { it.toInt() }
        } catch (e: Exception) {
            emptyList()
        }
    }
    
    fun setEqLevels(levels: List<Int>) {
        prefs.edit().putString("eq_levels", levels.joinToString(",")).apply()
        com.example.service.PlayerManager.applyAudioEffects(this)
    }
"""

content = content.replace("fun getNotificationPriority(): List<String> {", new_props + "\n    fun getNotificationPriority(): List<String> {")

with open("app/src/main/java/com/example/data/SettingsManager.kt", "w") as f:
    f.write(content)
