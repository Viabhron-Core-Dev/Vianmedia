import re

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

# Add formatTimeInput and parseTimeInput helpers
helpers = """private fun formatMs(ms: Long): String {
    val totalSeconds = ms / 1000
    val minutes = totalSeconds / 60
    val seconds = totalSeconds % 60
    return String.format("%02d:%02d", minutes, seconds)
}

private fun formatTimeInput(ms: Long): String {
    val totalSeconds = ms / 1000
    val hours = totalSeconds / 3600
    val minutes = (totalSeconds % 3600) / 60
    val seconds = totalSeconds % 60
    return String.format("%02d:%02d:%02d", hours, minutes, seconds)
}

private fun parseTimeInput(text: String): Long? {
    try {
        val parts = text.split(":")
        return when (parts.size) {
            3 -> {
                val h = parts[0].toLong()
                val m = parts[1].toLong()
                val s = parts[2].toLong()
                (h * 3600 + m * 60 + s) * 1000
            }
            2 -> {
                val m = parts[0].toLong()
                val s = parts[1].toLong()
                (m * 60 + s) * 1000
            }
            1 -> {
                val s = parts[0].toLong()
                s * 1000
            }
            else -> null
        }
    } catch (e: Exception) {
        return null
    }
}"""

content = content.replace("""private fun formatMs(ms: Long): String {
    val totalSeconds = ms / 1000
    val minutes = totalSeconds / 60
    val seconds = totalSeconds % 60
    return String.format("%02d:%02d", minutes, seconds)
}""", helpers)


# Update showTimeInputDialog triggers
content = content.replace("""timeInputText = ds1.toLong().toString(); showTimeInputDialog = "ds1\"""", """timeInputText = formatTimeInput(ds1.toLong()); showTimeInputDialog = "ds1\"""")
content = content.replace("""timeInputText = de1.toLong().toString(); showTimeInputDialog = "de1\"""", """timeInputText = formatTimeInput(de1.toLong()); showTimeInputDialog = "de1\"""")
content = content.replace("""timeInputText = ds2.toLong().toString(); showTimeInputDialog = "ds2\"""", """timeInputText = formatTimeInput(ds2.toLong()); showTimeInputDialog = "ds2\"""")
content = content.replace("""timeInputText = de2.toLong().toString(); showTimeInputDialog = "de2\"""", """timeInputText = formatTimeInput(de2.toLong()); showTimeInputDialog = "de2\"""")
content = content.replace("""timeInputText = start.toLong().toString(); showTimeInputDialog = "start\"""", """timeInputText = formatTimeInput(start.toLong()); showTimeInputDialog = "start\"""")
content = content.replace("""timeInputText = end.toLong().toString(); showTimeInputDialog = "end\"""", """timeInputText = formatTimeInput(end.toLong()); showTimeInputDialog = "end\"""")

# Update dialog UI
content = content.replace('title = { Text("Set Time (ms)") }', 'title = { Text("Set Time") }')
content = content.replace('if (it.isEmpty() || it.all { char -> char.isDigit() })', 'if (it.isEmpty() || it.all { char -> char.isDigit() || char == \':\' })')
content = content.replace('label = { Text("Milliseconds") }', 'label = { Text("HH:MM:SS") }')
content = content.replace('val parsed = timeInputText.toLongOrNull()', 'val parsed = parseTimeInput(timeInputText)')

with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
    f.write(content)

print("Updated time input formatting")
