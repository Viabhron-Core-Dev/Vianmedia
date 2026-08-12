import re

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'r') as f:
    content = f.read()

# 1. Add videoWidth and videoHeight state
state_block = r"var resizeMode by remember \{ androidx\.compose\.runtime\.mutableIntStateOf\(AspectRatioFrameLayout\.RESIZE_MODE_FIT\) \}"
new_state = """var resizeMode by remember { androidx.compose.runtime.mutableIntStateOf(AspectRatioFrameLayout.RESIZE_MODE_FIT) }
    var videoWidth by remember { androidx.compose.runtime.mutableIntStateOf(0) }
    var videoHeight by remember { androidx.compose.runtime.mutableIntStateOf(0) }"""
content = re.sub(state_block, new_state, content)

# 2. Add contentAlignment to the Box
box_start = r"Box\(modifier = Modifier\n        \.fillMaxSize\(\)\n        \.background\(Color\.Black\)\n        \.pointerInput\(mediaController, isLocked\) \{"
new_box_start = """Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
        .fillMaxSize()
        .background(Color.Black)
        .pointerInput(mediaController, isLocked) {"""
content = re.sub(box_start, new_box_start, content)

# 3. Update pipListener and controller listener to track video size
# We need to replace the PipHelper.updatePipParams with PipHelper... and videoWidth = w, videoHeight = h
size_change1 = r"PipHelper\.updatePipParams\(context, controller, w, h\)\n            \}"
new_size_change1 = """PipHelper.updatePipParams(context, controller, w, h)
                videoWidth = w
                videoHeight = h
            }"""
content = re.sub(size_change1, new_size_change1, content)

size_change2 = r"PipHelper\.updatePipParams\(context, player, w, h\)\n                \}"
new_size_change2 = """PipHelper.updatePipParams(context, player, w, h)
                    videoWidth = w
                    videoHeight = h
                }"""
content = re.sub(size_change2, new_size_change2, content)

size_change3 = r"PipHelper\.updatePipParams\(context, controller, w, h\)\n        val activity ="
new_size_change3 = """PipHelper.updatePipParams(context, controller, w, h)
        videoWidth = w
        videoHeight = h
        val activity ="""
content = re.sub(size_change3, new_size_change3, content)

# 4. Modify AndroidView to use modifier
android_view = r"AndroidView\(\n            factory = \{ ctx ->"
new_android_view = """val density = androidx.compose.ui.platform.LocalDensity.current.density
        AndroidView(
            modifier = if (resizeMode == 5 && videoWidth > 0 && videoHeight > 0) {
                Modifier.size((videoWidth / density).dp, (videoHeight / density).dp)
            } else {
                Modifier.fillMaxSize()
            },
            factory = { ctx ->"""
content = re.sub(android_view, new_android_view, content)

# 5. Modify view.resizeMode inside AndroidView
resize_mode_update = r"view\.resizeMode = resizeMode"
new_resize_mode_update = "view.resizeMode = if (resizeMode == 5) androidx.media3.ui.AspectRatioFrameLayout.RESIZE_MODE_FIT else resizeMode"
content = re.sub(resize_mode_update, new_resize_mode_update, content)

# 6. Update resizeMode cycling
resize_cycle = r"androidx\.media3\.ui\.AspectRatioFrameLayout\.RESIZE_MODE_ZOOM -> androidx\.media3\.ui\.AspectRatioFrameLayout\.RESIZE_MODE_FIXED_WIDTH"
new_resize_cycle = "androidx.media3.ui.AspectRatioFrameLayout.RESIZE_MODE_ZOOM -> 5"
content = re.sub(resize_cycle, new_resize_cycle, content)

with open('app/src/main/java/com/example/ui/screens/PlayerScreen.kt', 'w') as f:
    f.write(content)
