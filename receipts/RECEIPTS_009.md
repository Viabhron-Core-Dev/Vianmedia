2026-08-07T12:51:10Z
- Requested: User issued "Connect this to pip button in player also" to replace native PiP with the floating video player.
- Touched: app/src/main/java/com/example/ui/screens/PlayerScreen.kt, app/src/main/java/com/example/service/PlaybackService.kt, app/src/main/java/com/example/ui/components/FloatingVideoPlayerOverlay.kt
- Action: Modified `showOverlay` in `PlaybackService` to accept a boolean `startInVideoMode` flag which defaults to false. Mapped `ACTION_VIDEO_OVERLAY` widget command to launch `showOverlay(true)`. Replaced the native Android `enterPictureInPictureMode` logic in the `PlayerScreen`'s PiP button with sending `ACTION_VIDEO_OVERLAY` and closing the main activity, making the app rely solely on the custom floating video player overlay. Corrected missing imports in `FloatingVideoPlayerOverlay.kt`.
- Verification: local build only
