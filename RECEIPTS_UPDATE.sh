cat << 'INNER_EOF' >> receipts/RECEIPTS_001.md
2026-08-03T10:59:00Z
Enhanced batch image compression to support custom quality, formats, and orientation-aware scaling.
Touched: app/src/main/java/com/example/ui/components/CompressionOptionsDialog.kt, app/src/main/java/com/example/ui/navigation/AppNavigation.kt, app/src/main/java/com/example/BatchActionActivity.kt, app/src/main/java/com/example/service/CompressionService.kt
Updated the UI to include a slider for JPEG/PNG/WebP format selection and 0-100% quality adjustment. Fixed the landscape scaling bug by making the bounding box boundaries orientation-aware (so VGA bounds rotate to match portrait vs landscape).
Verified by local build.
INNER_EOF
