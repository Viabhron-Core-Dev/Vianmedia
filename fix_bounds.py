with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "r") as f:
    content = f.read()

old_block = """                            editState = when (showTimeInputDialog) {
                                "ds1" -> editState.copy(doubleTrimStart1Ms = p)
                                "de1" -> editState.copy(doubleTrimEnd1Ms = p.coerceAtLeast(editState.doubleTrimStart1Ms))
                                "ds2" -> editState.copy(doubleTrimStart2Ms = p.coerceAtLeast(editState.doubleTrimEnd1Ms))
                                "de2" -> editState.copy(doubleTrimEnd2Ms = p.coerceAtLeast(editState.doubleTrimStart2Ms))
                                "start" -> editState.copy(trimStartMs = p)
                                "end" -> editState.copy(trimEndMs = p.coerceAtLeast(editState.trimStartMs))
                                else -> editState
                            }"""

new_block = """                            editState = when (showTimeInputDialog) {
                                "ds1" -> editState.copy(doubleTrimStart1Ms = p, doubleTrimEnd1Ms = editState.doubleTrimEnd1Ms.coerceAtLeast(p))
                                "de1" -> editState.copy(doubleTrimEnd1Ms = p.coerceAtLeast(editState.doubleTrimStart1Ms))
                                "ds2" -> editState.copy(doubleTrimStart2Ms = p.coerceAtLeast(editState.doubleTrimEnd1Ms), doubleTrimEnd2Ms = editState.doubleTrimEnd2Ms.coerceAtLeast(p.coerceAtLeast(editState.doubleTrimEnd1Ms)))
                                "de2" -> editState.copy(doubleTrimEnd2Ms = p.coerceAtLeast(editState.doubleTrimStart2Ms))
                                "start" -> editState.copy(trimStartMs = p, trimEndMs = editState.trimEndMs.coerceAtLeast(p).takeIf { it > 0 } ?: durationMs)
                                "end" -> editState.copy(trimEndMs = p.coerceAtLeast(editState.trimStartMs))
                                else -> editState
                            }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt", "w") as f:
        f.write(content)
    print("Fixed bounds logic")
else:
    print("Could not find block")
