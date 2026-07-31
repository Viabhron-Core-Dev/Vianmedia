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
2026-07-31T09:47:00Z
- Requested: "Fix grey box remaining landscape when video is rotated 90 or 270 degrees in the preview"
- Files touched: app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt
- Action:
  1. Updated the preview container in `VideoEditorScreen.kt`. Replaced the previous `previewModifier` logic which applied the `background(Color.DarkGray)` to the landscape-sized bounds.
  2. Wrapped `AndroidView` in a `Box` that represents the visual (rotated) bounds of the video, and applied the background there. 
  3. Ensured that `AndroidView` calculates its internal landscape size and is rotated 90/270 degrees *within* the correctly sized portrait `Box`.
  4. Updated the Canvas crop overlay bounds calculation (`videoAspect`) to use `effectiveVideoWidth` and `effectiveVideoHeight` depending on the current rotation state. This prevents the crop overlay from drawing out-of-bounds or using the unrotated aspect ratio.
- Verification: Local build only.
2026-07-31T09:47:00Z
- Requested: "Cut tool custom text input should be divided between h: m: s not like now milk second."
- Files touched: app/src/main/java/com/example/ui/screens/VideoEditorScreen.kt
- Action:
  1. Added `formatTimeInput` and `parseTimeInput` helper functions to convert back and forth between milliseconds and `HH:MM:SS` format.
  2. Replaced `.toLong().toString()` calls when triggering `showTimeInputDialog` with calls to `formatTimeInput`.
  3. Modified the `OutlinedTextField` inside the `showTimeInputDialog` `AlertDialog` to accept digits and colons (`:`), updated its label to "HH:MM:SS", and changed parsing from `toLongOrNull()` to use the new `parseTimeInput(timeInputText)` function.
- Verification: Local build only.
2026-07-31T10:56:00Z
- Requested: "Player opening video portrait even when video landscape. See how nextplayer does it."
- Files touched: app/src/main/java/com/example/ui/screens/PlayerScreen.kt
- Action:
  1. Found that `unappliedRotationDegrees` can misinterpret orientation for some video files when determining the requested screen orientation.
  2. Analyzed NextPlayer's source code and found they simply rely on `videoSize.height > videoSize.width` to classify a video as portrait. 
  3. Replaced the `effectiveWidth`/`effectiveHeight` calculation in `updateOrientation` and the initial check in `PlayerScreen.kt` with a direct comparison: if `height > width` it requests `SENSOR_PORTRAIT`, else it requests `SENSOR_LANDSCAPE`.
- Verification: Local build only.
2026-07-31T11:11:31Z
- Requested: "Check widget. It uses different icons for same things then mini player. Check the file explorer. It is wrong. Want it to be like coptly of mini player explorer. Want both to look more or less same."
- Files touched: app/src/main/res/drawable/* (ic_widget_*.xml), app/src/main/res/layout/widget_media.xml, app/src/main/res/layout/widget_list_item.xml, app/src/main/java/com/example/widget/MediaWidgetService.kt, app/src/main/java/com/example/widget/MediaWidgetProvider.kt
- Action:
  1. Replaced the custom widget drawables with Material icon path vectors that match the mini player's UI (e.g., skip_previous, fast_rewind, play_arrow, fast_forward, skip_next, stop, shuffle, repeat, refresh, search, close, open_in_full).
  2. Updated `widget_media.xml` to use the new icons for the playback controls and action bar (replacing the generic @android:drawable/ resources).
  3. Modified `widget_list_item.xml` to include an icon `ImageView` (visible only for root level items).
  4. Rewrote `MediaWidgetService.kt` to mirror the `MiniPlayerOverlay` hierarchy. It now has `explorer_mode` ("root", "current", "folders", "folder_items", "playlists") and navigates exactly like the mini player.
  5. Updated `MediaWidgetProvider.kt` to handle the navigation intents (NAVIGATE_CURRENT, NAVIGATE_FOLDERS, NAVIGATE_PLAYLISTS, ACTION_BACK_FOLDER) and update the widget UI state (`widget_explorer_title` and back button visibility).
- Verification: Local build only.
