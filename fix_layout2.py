import sys

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'r') as f:
    content = f.read()

target = """.androidx.compose.ui.layout.layout { measurable, constraints ->"""
replacement = """.androidx.compose.ui.layout.layout { measurable, constraints ->"""

# Actually, layout is an extension function: `import androidx.compose.ui.layout.layout`
# So we should just use `.layout { measurable, constraints ->` and add the import.

content = content.replace(target, ".layout { measurable, constraints ->")

if "import androidx.compose.ui.layout.layout" not in content:
    content = content.replace("import androidx.compose.ui.graphics.graphicsLayer", "import androidx.compose.ui.graphics.graphicsLayer\nimport androidx.compose.ui.layout.layout")

# The Constraints class also needs to be imported or fully qualified correctly.
content = content.replace("androidx.compose.ui.unit.Constraints.fixed", "androidx.compose.ui.unit.Constraints.fixed")
# Let's fix the unresolved reference `maxHeight` on constraints. 
# It should be `constraints.maxHeight` and `constraints.maxWidth`

# Wait, `measure` doesn't take constraints? 
# "Cannot access 'fun RowColumnMeasurePolicy.measure(...): MeasureResult': it is internal in file."
# This is because I used `measurable.measure(...)` but the compiler resolved `measure` to some other internal function.
# Wait! In Compose, `.layout { measurable, constraints ->` gives a Measurable and Constraints.
# You call `measurable.measure(constraints)` to get a Placeable.
# Let's write the Modifier.layout block cleanly.

replacement_block = """                                .layout { measurable, constraints ->
                                    if (editState.rotateConfig % 180 != 0) {
                                        val placeable = measurable.measure(
                                            androidx.compose.ui.unit.Constraints.fixed(constraints.maxHeight, constraints.maxWidth)
                                        )
                                        layout(constraints.maxWidth, constraints.maxHeight) {
                                            val x = (constraints.maxWidth - placeable.width) / 2
                                            val y = (constraints.maxHeight - placeable.height) / 2
                                            placeable.placeRelative(x, y)
                                        }
                                    } else {
                                        val placeable = measurable.measure(constraints)
                                        layout(placeable.width, placeable.height) {
                                            placeable.placeRelative(0, 0)
                                        }
                                    }
                                }"""

# Let's replace the block.
import re
pattern = r"\.layout\s*\{\s*measurable,\s*constraints\s*->[\s\S]*?place\([^)]*\)\s*\}\s*\}\s*\}"
content = re.sub(pattern, replacement_block.strip(), content)

with open('app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt', 'w') as f:
    f.write(content)
