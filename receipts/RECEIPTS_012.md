2026-08-07T13:52:00Z
- Requested: Fix jerky m4s video files playing and editing.
- Touched: app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt
- Action: Added `m4s` to the automatic pre-conversion pipeline in `VideoEditorScreen`. Now, when an `m4s` file is opened in the editor, FFmpeg automatically remuxes it (`-vcodec libx264 -preset ultrafast -crf 23 -acodec aac`) into a standard `.mp4` container with proper indexes and keyframes. This resolves the jerkiness and seeking issues caused by raw DASH/HLS segments lacking standalone `moov` atoms.
- Verification: local build only
