2026-08-07T12:58:00Z
- Requested: Connect the new overlay to PiP button in main player and widget.
- Touched: app/src/main/java/com/example/widget/MediaWidgetProvider.kt, app/src/main/java/com/example/service/PlaybackService.kt
- Action: Updated `MediaWidgetProvider` to intercept `ACTION_PIP` and broadcast `ACTION_VIDEO_OVERLAY` to the `PlaybackService`. Updated the media notification custom PiP command handler in `PlaybackService` to launch the video overlay (`showOverlay(true)`) instead of broadcasting the native PiP intent. 
- Verification: local build only
