2026-08-07T13:08:00Z
- Requested: Player still giving that landscape to portrait on second. Not sure why. How about connecting log keeper for this. Also on start video should always do a quick lightweight check.
- Touched: app/src/main/java/com/example/ui/screens/PlayerScreen.kt
- Action: Implemented a lightweight background `MediaMetadataRetriever` check immediately upon entering `PlayerScreen` to determine true video dimensions and set `requestedOrientation` correctly. Removed the direct call to `updateOrientation(controller.videoSize)` on initial startup, as it was passing the cached dimensions of the previously played video (since the new media item takes ~1 second to parse), causing the momentary "flash" to incorrect orientation. Added extensive `LogKeeper` logging to `updateOrientation` and the lightweight dimension checker for future debugging.
- Verification: local build only
