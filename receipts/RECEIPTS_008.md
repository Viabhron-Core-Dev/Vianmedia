2026-08-07T12:22:00Z
- Requested: User issued "Implement" to implement the floating window video player as a substitute for PiP.
- Touched: app/src/main/java/com/example/ui/components/MiniPlayerOverlay.kt, app/src/main/java/com/example/ui/components/FloatingVideoPlayerOverlay.kt, app/src/main/java/com/example/service/PlaybackService.kt
- Action: Created `FloatingVideoPlayerOverlay` with a top bar (drag, double-tap to open main player, switch to mini player), a main `PlayerView` maintaining the video aspect ratio naturally with its standard playback controls, and bottom-right floating buttons for close, minimize, and resize. Updated `PlaybackService` to maintain an `isVideoMode` state and dynamically switch between `MiniPlayerOverlay` and `FloatingVideoPlayerOverlay`, preserving their exact size/position. Updated `MiniPlayerOverlay` to feature a button for switching back to the floating video player.
- Verification: local build only
