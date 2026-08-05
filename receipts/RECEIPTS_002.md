2026-08-05T09:10:00Z
- Requested: User asked to investigate why PiP is not working and to discuss only without writing code.
- Touched: None (Discussion only).
- Action: Analyzed `MainActivity.kt`, `PipHelper.kt`, and `PlayerScreen.kt`. Found that `updatePipParams` fails due to `context as? Activity` casting bug with Compose `ContextWrapper`. Found that `MainActivity` lacks `onUserLeaveHint` override.
- Verification: not tested (discussion)
