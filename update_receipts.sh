mkdir -p receipts
cat << 'RECEIPT' >> receipts/RECEIPTS_001.md
2026-08-01T05:36:00Z
Fixed video orientation bug where landscape videos play in portrait, and the screen gets stuck in the previous video's orientation.
Touched: app/src/main/java/com/example/ui/screens/PlayerScreen.kt
Implemented correct orientation detection by factoring in `videoSize.unappliedRotationDegrees` to determine the true effective orientation of the video (fixing the core bug where videos rotated via metadata were forced into the wrong orientation). Also removed the faulty initial block and `EVENT_MEDIA_ITEM_TRANSITION` triggers that were forcing the orientation to change using a stale `videoSize` from the previously played media item.
Verified by local build.
RECEIPT
