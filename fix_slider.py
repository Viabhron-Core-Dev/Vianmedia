with open("app/src/main/java/com/example/ui/screens/AudioSettingsScreen.kt", "r") as f:
    content = f.read()

old_slider = """                                Slider(
                                    value = eqLevels[i].toFloat(),
                                    onValueChange = { 
                                        val newList = eqLevels.toMutableList()
                                        newList[i] = it.roundToInt()
                                        eqLevels = newList
                                        settingsManager.setEqLevels(newList)
                                    },
                                    valueRange = -1500f..1500f,
                                    modifier = Modifier.height(150.dp),
                                    colors = SliderDefaults.colors(
                                        thumbColor = MaterialTheme.colorScheme.primary,
                                        activeTrackColor = MaterialTheme.colorScheme.primary,
                                        inactiveTrackColor = MaterialTheme.colorScheme.surfaceVariant
                                    )
                                )"""

new_slider = """                                Box(
                                    modifier = Modifier
                                        .height(150.dp)
                                        .width(40.dp),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Slider(
                                        value = eqLevels[i].toFloat(),
                                        onValueChange = { 
                                            val newList = eqLevels.toMutableList()
                                            newList[i] = it.roundToInt()
                                            eqLevels = newList
                                            settingsManager.setEqLevels(newList)
                                        },
                                        valueRange = -1500f..1500f,
                                        modifier = Modifier
                                            .width(150.dp)
                                            .height(40.dp)
                                            .androidx.compose.ui.graphics.graphicsLayer {
                                                rotationZ = -90f
                                                transformOrigin = androidx.compose.ui.graphics.TransformOrigin(0.5f, 0.5f)
                                            },
                                        colors = SliderDefaults.colors(
                                            thumbColor = MaterialTheme.colorScheme.primary,
                                            activeTrackColor = MaterialTheme.colorScheme.primary,
                                            inactiveTrackColor = MaterialTheme.colorScheme.surfaceVariant
                                        )
                                    )
                                }"""

content = content.replace(old_slider, new_slider)

with open("app/src/main/java/com/example/ui/screens/AudioSettingsScreen.kt", "w") as f:
    f.write(content)
