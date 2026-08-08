2026-08-08T01:23:00Z
- Requested: Move aspect ratio presets from "Aspect Ratio" to "Crop" (which act as exact crop boxes), and make the "Aspect Ratio" tool purely stretch/warp the video without cropping.
- Touched: app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt
- Action: Updated the UI choices for Aspect Ratio and Crop tools. The Crop tool now handles "16:9", "9:16", "1:1", "4:3", "21:9", and "Custom". The Aspect Ratio tool now handles stretching using `Presentation.LAYOUT_STRETCH_TO_FIT` (2) in the `ExoPlayer` live preview, and generates a corresponding `scale=w=max(...):h=max(...),setsar=1` FFmpeg string for export, successfully squeezing or stretching the video dimensions without cutting pixels. Fixed the crop preview math to use center-cropping when preset aspect ratios are selected, and modified export orientation logic to detect aspect ratio intent correctly.
- Verification: local build only
