import re

with open("app/src/main/java/com/example/ui/screens/AudioSettingsScreen.kt", "r") as f:
    content = f.read()

old_mod = ".androidx.compose.ui.graphics.graphicsLayer {"
new_mod = ".androidx.compose.ui.graphics.graphicsLayer.graphicsLayer {"
content = content.replace(old_mod, new_mod)

old_mod2 = ".graphicsLayer.graphicsLayer"
new_mod2 = ".graphicsLayer"
content = content.replace(old_mod2, new_mod2)

# Oh wait, we just need to import androidx.compose.ui.graphics.graphicsLayer
content = content.replace("import androidx.compose.ui.platform.LocalContext", "import androidx.compose.ui.platform.LocalContext\nimport androidx.compose.ui.graphics.graphicsLayer\nimport androidx.compose.ui.graphics.TransformOrigin")

old_slider_mod = """                                        modifier = Modifier
                                            .width(150.dp)
                                            .height(40.dp)
                                            .androidx.compose.ui.graphics.graphicsLayer {
                                                rotationZ = -90f
                                                transformOrigin = androidx.compose.ui.graphics.TransformOrigin(0.5f, 0.5f)
                                            },"""

new_slider_mod = """                                        modifier = Modifier
                                            .width(150.dp)
                                            .height(40.dp)
                                            .graphicsLayer {
                                                rotationZ = -90f
                                                transformOrigin = TransformOrigin(0.5f, 0.5f)
                                            },"""

content = content.replace(old_slider_mod, new_slider_mod)

with open("app/src/main/java/com/example/ui/screens/AudioSettingsScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/service/PlayerManager.kt", "r") as f:
    content = f.read()

# DynamicsProcessing.MbcBand(boolean enabled, float cutoffFrequency, float attackTime, float releaseTime, float ratio, float threshold, float kneeWidth, float noiseGateThreshold, float expanderRatio, float preGain, float postGain)
old_mbc = "val mbcBand = DynamicsProcessing.MbcBand(true, 1000f, -40f, 10f, -50f, 4f, -40f, 4f)"
new_mbc = "val mbcBand = DynamicsProcessing.MbcBand(true, 1000f, 50f, 200f, 4f, -40f, 10f, -90f, 1f, 0f, 5f)"
content = content.replace(old_mbc, new_mbc)

with open("app/src/main/java/com/example/service/PlayerManager.kt", "w") as f:
    f.write(content)
