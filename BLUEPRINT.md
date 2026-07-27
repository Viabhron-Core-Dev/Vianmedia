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

## Recent Changes
- Changed floating window minimized icon to perfectly mirror the app's launcher icon.
- Styled Mini Player colors to match Library TopAppBar (Surface color header, subtle primary borders).
- Changed floating window playback buttons to black/onSurface instead of blue.
- Fixed translationY animations to prevent glitchy post-drop reshreshuffling in Playlist view.
