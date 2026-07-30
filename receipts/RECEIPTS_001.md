2026-07-30T10:31:00Z
- Requested: Fix the rotation preview not rotating the video but instead cropping it to portrait.
- Files touched: app/src/main/res/layout/player_view_texture.xml, app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt
- Action:
  1. Created a layout XML for PlayerView specifying `app:surface_type="texture_view"`.
  2. Modified VideoEditorScreen to inflate this TextureView-based PlayerView. This ensures `graphicsLayer` transformations (like `rotationZ`) correctly apply to the video rendering surface, unlike `SurfaceView` which is drawn on a separate WindowManager layer and ignores Compose clipping/rotation.
  3. Replaced the `rotScale` shrinkage logic. Wrapped the preview in a `BoxWithConstraints` to mathematically calculate the exact unrotated bounds (`fitHeight x fitWidth`) needed so that, when rotated 90/270 degrees, the visual bounds perfectly maximize the parent screen dimensions without arbitrary scaling or cropping.
- Verification: Local build only.
2026-07-30T11:58:00Z
- Requested: Fix "Playing any video from other app opens Library but then quickly opens player", fix "Cropping video adds black bars", fix "Video of portrait still being exported as landscape".
- Files touched: app/src/main/java/com/example/ui/navigation/AppNavigation.kt, app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt
- Action:
  1. Updated `AppNavigation.kt` to use `intentDest ?: startDest` directly as `startDestination` in `NavHost`, preventing the initial flash of the Library screen when launched from a file explorer intent.
  2. Fixed portrait rotation detection in `VideoEditorScreen.kt` by evaluating `videoSize.unappliedRotationDegrees` in `onVideoSizeChanged`. This ensures `videoWidth` and `videoHeight` always reflect the visual display orientation rather than the encoded dimensions.
  3. Fixed black bars on exported cropped videos. Removed the `pad` filter in FFmpeg export and correctly inferred the post-crop bounding box. By stripping `pad` and ensuring even dimensions (`scale=trunc(iw/2)*2:trunc(ih/2)*2`), custom crops are exported in their exact aspect ratio without being letterboxed into a standard 16:9 container.
- Verification: Local build only.
2026-07-30T12:33:00Z
- Requested: "compare widget to mini player. Icons/buttons should be same also bottom file explorer is missing the back and the hierarchy of mini player."
- Files touched: app/src/main/res/layout/widget_media.xml, app/src/main/java/com/example/widget/MediaWidgetProvider.kt, app/src/main/java/com/example/widget/MediaWidgetService.kt, and several drawable files.
- Action:
  1. Updated `widget_media.xml` to match the MiniPlayer's hierarchy. Added Rewind, Fast Forward, and Stop buttons to the playback controls row. Added a back button and a title bar to the file explorer list area.
  2. Created drawable assets (`ic_widget_rewind.xml`, `ic_widget_fastforward.xml`, `ic_widget_stop.xml`, `ic_widget_back.xml`, `ic_widget_refresh.xml`) for the new widget actions.
  3. Modified `MediaWidgetProvider.kt` to handle the new action intents (`ACTION_REWIND`, `ACTION_FFWD`, `ACTION_STOP`, `ACTION_BACK_FOLDER`). Added logic to dynamically show/hide the back button and update the list title based on whether the player is active, inside a folder, or at the root folder level.
  4. Updated `MediaWidgetService.kt` so the "up" directory button inside `folderItems` is removed in favor of the new explicit back button in the header layout.
- Verification: Local build only.
