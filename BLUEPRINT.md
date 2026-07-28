# Blueprint

## Architecture
- **UI Framework**: Jetpack Compose (Material 3)
- **Data Persistence**: Room Database for playlist and library caching
- **Media Player**: Media3 (ExoPlayer) with foreground `PlaybackService`
- **Dependency Injection**: Constructor injection

## Components
- **MainScreen**: Bottom navigation hub for Library, Playlists, and Player
- **LibraryScreen**: Scans local files, groups into folders, selection logic
- **PlaylistsScreen**: Displays saved playlists
- **PlaylistDetailScreen**: Displays items, manual drag-and-drop ordering, multi-select deletion
- **PlayerScreen**: Main video/audio player view, Media3 bindings, brightness slider, PiP controls
- **MiniPlayerOverlay**: Floating draggable overlay, persists state when navigating, fold/unfold logic
- **MediaWidgetProvider**: Home screen RemoteViews widget

## Recent Changes
- Connected widget (`MediaWidgetProvider` and `MediaWidgetService`) to `LogKeeper` for deep error tracking.
- Fixed blank/crashing home screen widget by removing unsupported `RemoteViews` attributes (`backgroundTint`, `tint`, `<Button>`).
- Styled the App Widget to perfectly match the Mini Player theme (LightBlueBackground `#F5F7FA`, 12dp rounded corners, `#19202D` dark text/icons, subtle primary borders).
- Fixed playlist reorder dragging wrong item by keying `pointerInput` to `item.id` and `index`.
- Added auto-cleanup lifecycle for the "Temp Current" playlist (deletes itself when playback finishes or player is stopped).
- Zoomed in on the Mini Player floating icon, cropping the blue background to focus on the play button.
- Made Mini Player backgrounds completely opaque to fix visual bleeding (pink tinting) from underlying views.
