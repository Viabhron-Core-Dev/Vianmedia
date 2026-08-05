2026-08-04T15:47:00Z
- Requested: User asked to just discuss and verify if the orientation fix is 100% sound.
- Touched: None (Discussion only).
- Action: Analyzed ExoPlayer `EVENT_VIDEO_SIZE_CHANGED` behavior and confirmed that identical consecutive video resolutions caused the previous event to drop. Confirmed that adding `EVENT_MEDIA_ITEM_TRANSITION` mathematically fixes the edge case.
- Verification: not tested (discussion)
