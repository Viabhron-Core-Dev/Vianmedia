2026-08-06T14:25:00Z
- Requested: User reported m4s files renamed to mp4 fail to load in the video editor. Requested to "just discuss no coding".
- Touched: None
- Action: Analyzed the issue conceptually. Explained that m4s files are fragmented MP4 segments lacking the `moov` initialization atom, which ExoPlayer requires for local playback, whereas other editors might use robust parsers like FFmpeg that can guess the stream properties. No code changes made.
- Verification: not tested (discussion only)
