package com.example.service
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import com.example.data.AppDatabase
import com.example.data.PlaylistRepository

fun clearTempPlaylist(context: android.content.Context) {
    CoroutineScope(Dispatchers.IO).launch {
        try {
            val db = AppDatabase.getDatabase(context)
            val repo = PlaylistRepository(db.playlistDao())
            val temp = repo.getPlaylistByNameSync("Temp Current")
            if (temp != null) {
                repo.deletePlaylistById(temp.id)
            }
        } catch (e: Exception) {}
    }
}
