# BLUEPRINT

## Phase 1: Foundation (Completed)
- Setup basic app structure and dependencies
- Implement ExoPlayer/Media3 for video and audio playback
- Create unified PlayerScreen for all media types
- Integrate File Explorer for media selection

## Phase 2: Core Features (Completed)
- Implement background playback service (MediaSessionService)
- Add Picture-in-Picture (PiP) support
- Add Mini Player overlay permission flow and basic service overlay
- Add Media Widget for home screen control and file browsing
- Support subtitle tracks (SRT, VTT) and custom font settings
- Add volume booster (LoudnessEnhancer)

## Phase 3: Video & Photo Editing (Completed/In Progress)
- Implement `VideoEditorScreen` with basic UI layout
- Add FFmpeg integration for video processing
- Implement Crop tool (Custom aspect ratio support with draggable corners)
- Implement Trim/Cut tool (Timeline track with skip-middle cut functionality)
- Implement Video Conversion/Export tool (Resolution, FPS, ultrafast presets)
- Refine RightTools UI layout in `PlayerScreen` for compactness

## Phase 4: UI/UX Refinement
- Improve visual feedback for widget actions
- Ensure thread safety in all background operations

## Progress Update
- Fixed widget thread exceptions and interaction dead-states by utilizing MediaController async initialization.
- Fixed widget incorrectly falling back to File Explorer mode when the media player was paused.
- Refactored Widget layout to include PiP, Expand, Close, Open MiniPlayer, and Search controls.
- Created translucent WidgetSearchActivity to perform widget-based file search without triggering full UI.
- Implemented tap-and-type minute adjustments for start and end times in the Trim/Cut tool.
- Dynamically swapped the RangeSlider track colors so that in Cut (Remove Middle) mode, the active track visually fills the outside ranges instead of the middle.
- Implemented a post-export modal dialog in the Video Editor with a portrait preview player.
- Added an "Edit Finished File" button to the preview modal to recursively open the exported video back into the editor.

- Synchronized Media Widget UI and icon set to perfectly mirror the internal Mini Player overlay structure.
- Fixed ReceiverCallNotAllowedException in widget by using applicationContext for MediaController.
- Synced widget File Explorer visual and logical states with MiniPlayer, including active item highlights and 'Feature coming soon' placeholders.- Fixed an orientation bug where subsequent video loads incorrectly fell back to landscape instead of auto-detecting orientation by using the properly decoded URI for comparison.
- Updated the Crop tool UI logic so that Center Crop and Aspect Ratio presets display the darkened overlay blocks (to show what's being cut out) without draggable handles, which are reserved for the Custom preset.
- Implemented **Audio & Sound Effects** features:
  - **Vocal Frequency EQ**: 5-band equalizer with presets for flat and vocal boost.
  - **Dynamic Range Compression (Night Mode)**: Uses `DynamicsProcessing` to level audio (quiet sounds boosted, loud sounds reduced).
  - **Center Channel Extraction**: Custom `AudioProcessor` that isolates the mid-channel, acting like a reverse karaoke effect to enhance dialogue.
- **Bug Fix**: Fixed the auto-rotation video orientation logic to properly account for `unappliedRotationDegrees` (the "NextPlayer method"). This ensures videos filmed in portrait mode on phones actually trigger vertical auto-rotation properly instead of sideways landscape.
- **Bug Fix**: Reverted orientation handling logic to `SCREEN_ORIENTATION_UNSPECIFIED`. Removed the forced programmatic locks based on video dimensions to let the device's native auto-rotate sensors take full control.
- **Bug Fix & Enhancement**: Enhanced batch image compression to support custom quality (10-100%), formats (JPEG, PNG, WebP), and orientation-aware scaling bounds (fixing the landscape scaling issue).
