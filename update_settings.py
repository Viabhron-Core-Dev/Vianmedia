import re

with open("app/src/main/java/com/example/data/SettingsManager.kt", "r") as f:
    content = f.read()

new_methods = """    fun getStoredDuration(uri: String): Long {
        return prefs.getLong("dur_$uri", -1L)
    }

    fun saveVideoOrientation(uri: String, isPortrait: Boolean) {
        prefs.edit().putBoolean("orient_$uri", isPortrait).apply()
    }

    fun getVideoOrientation(uri: String): Boolean? {
        return if (prefs.contains("orient_$uri")) {
            prefs.getBoolean("orient_$uri", false)
        } else {
            null
        }
    }

    fun removePlaybackState(uri: String) {
        prefs.edit()
            .remove("time_$uri")
            .remove("pos_$uri")
            .remove("dur_$uri")
            .remove("orient_$uri")
            .apply()
    }"""

content = content.replace('    fun getStoredDuration(uri: String): Long {\n        return prefs.getLong("dur_$uri", -1L)\n    }', new_methods)

with open("app/src/main/java/com/example/data/SettingsManager.kt", "w") as f:
    f.write(content)

print("Updated SettingsManager")
