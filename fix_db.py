import sys

# 1. Update PlaylistItem.kt
with open('app/src/main/java/com/example/data/PlaylistItem.kt', 'r') as f:
    content = f.read()

target = "val timestamp: Long = System.currentTimeMillis()"
if target in content:
    content = content.replace(target, "val timestamp: Long = System.currentTimeMillis(),\n    val isNotFound: Boolean = false")
    with open('app/src/main/java/com/example/data/PlaylistItem.kt', 'w') as f:
        f.write(content)
    print("Updated PlaylistItem.kt")
else:
    print("Could not update PlaylistItem.kt")

# 2. Update AppDatabase.kt
with open('app/src/main/java/com/example/data/AppDatabase.kt', 'r') as f:
    content = f.read()

content = content.replace("version = 2", "version = 3")

target_mig = """                val MIGRATION_1_2 = object : androidx.room.migration.Migration(1, 2) {
                    override fun migrate(db: androidx.sqlite.db.SupportSQLiteDatabase) {
                        db.execSQL("ALTER TABLE playlists ADD COLUMN orderIndex INTEGER NOT NULL DEFAULT 0")
                    }
                }"""
replacement_mig = """                val MIGRATION_1_2 = object : androidx.room.migration.Migration(1, 2) {
                    override fun migrate(db: androidx.sqlite.db.SupportSQLiteDatabase) {
                        db.execSQL("ALTER TABLE playlists ADD COLUMN orderIndex INTEGER NOT NULL DEFAULT 0")
                    }
                }
                val MIGRATION_2_3 = object : androidx.room.migration.Migration(2, 3) {
                    override fun migrate(db: androidx.sqlite.db.SupportSQLiteDatabase) {
                        db.execSQL("ALTER TABLE playlist_items ADD COLUMN isNotFound INTEGER NOT NULL DEFAULT 0")
                    }
                }"""

if target_mig in content:
    content = content.replace(target_mig, replacement_mig)
    content = content.replace(".addMigrations(MIGRATION_1_2)", ".addMigrations(MIGRATION_1_2, MIGRATION_2_3)")
    with open('app/src/main/java/com/example/data/AppDatabase.kt', 'w') as f:
        f.write(content)
    print("Updated AppDatabase.kt")
else:
    print("Could not update AppDatabase.kt")
