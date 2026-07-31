package com.example.widget

import android.content.Context
import android.content.Intent
import android.widget.RemoteViews
import android.widget.RemoteViewsService
import com.example.R
import com.example.service.PlayerManager
import androidx.media3.common.MediaItem
import com.example.data.MediaRepository
import com.example.data.MediaFolder
import kotlinx.coroutines.runBlocking

class MediaWidgetService : RemoteViewsService() {
    override fun onGetViewFactory(intent: Intent): RemoteViewsFactory {
        return MediaWidgetFactory(this.applicationContext)
    }
}

class MediaWidgetFactory(private val context: Context) : RemoteViewsService.RemoteViewsFactory {
    private var playlist = listOf<MediaItem>()
    private var folders = listOf<MediaFolder>()
    private var folderItems = listOf<com.example.data.MediaItem>()
    
    private var currentMode = "root"
    private var folderId: String? = null

    override fun onCreate() {}

    override fun onDataSetChanged() {
        try {
            val prefs = context.getSharedPreferences("widget_prefs", Context.MODE_PRIVATE)
            currentMode = prefs.getString("explorer_mode", "current") ?: "current"
            folderId = prefs.getString("folder_id", null)
            val searchQuery = prefs.getString("search_query", "") ?: ""

            // Always fetch the current playlist in case it's needed
            val items = mutableListOf<MediaItem>()
            runBlocking {
                kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                    val player = PlayerManager.exoPlayer
                    if (player != null && !player.currentTimeline.isEmpty) {
                        for (i in 0 until player.currentTimeline.windowCount) {
                            val window = androidx.media3.common.Timeline.Window()
                            player.currentTimeline.getWindow(i, window)
                            items.add(window.mediaItem)
                        }
                    }
                }
            }
            playlist = items

            if (searchQuery.isNotBlank()) {
                currentMode = "search_results"
                runBlocking {
                    val repo = MediaRepository(context)
                    val allFolders = repo.getMediaFolders()
                    val allItems = allFolders.flatMap { it.mediaItems }
                    folderItems = allItems.filter { it.name.contains(searchQuery, ignoreCase = true) }
                }
            } else if (currentMode == "folders" || currentMode == "folder_items") {
                runBlocking {
                    val repo = MediaRepository(context)
                    folders = repo.getMediaFolders()
                    if (folderId != null) {
                        folderItems = folders.find { it.id == folderId }?.mediaItems ?: emptyList()
                        currentMode = "folder_items"
                    } else {
                        currentMode = "folders"
                    }
                }
            }
        } catch (e: Exception) {
            com.example.LogKeeper.logError("MediaWidgetFactory", "Error in onDataSetChanged", e)
        }
    }

    override fun onDestroy() {}

    override fun getCount(): Int {
        return when (currentMode) {
            "root" -> 3
            "current" -> playlist.size
            "folders" -> folders.size
            "folder_items", "search_results" -> folderItems.size
            "playlists" -> 0 // Placeholder
            else -> 0
        }
    }

    override fun getViewAt(position: Int): RemoteViews {
        try {
            val views = RemoteViews(context.packageName, R.layout.widget_list_item)
            
            // Set defaults
            views.setViewVisibility(R.id.widget_item_icon, android.view.View.VISIBLE)
            
            when (currentMode) {
                "root" -> {
                    when (position) {
                        0 -> {
                            views.setTextViewText(R.id.widget_item_title, "Current")
                            views.setImageViewResource(R.id.widget_item_icon, R.drawable.ic_widget_play_circle)
                            views.setOnClickFillInIntent(R.id.widget_item_root, Intent().putExtra("WIDGET_ACTION", "NAVIGATE_CURRENT"))
                        }
                        1 -> {
                            views.setTextViewText(R.id.widget_item_title, "Folder List")
                            views.setImageViewResource(R.id.widget_item_icon, R.drawable.ic_widget_folder)
                            views.setOnClickFillInIntent(R.id.widget_item_root, Intent().putExtra("WIDGET_ACTION", "NAVIGATE_FOLDERS"))
                        }
                        2 -> {
                            views.setTextViewText(R.id.widget_item_title, "Playlists")
                            views.setImageViewResource(R.id.widget_item_icon, R.drawable.ic_widget_playlist)
                            views.setOnClickFillInIntent(R.id.widget_item_root, Intent().putExtra("WIDGET_ACTION", "NAVIGATE_PLAYLISTS"))
                        }
                    }
                }
                "current" -> {
                    views.setViewVisibility(R.id.widget_item_icon, android.view.View.GONE)
                    val item = playlist[position]
                    views.setTextViewText(R.id.widget_item_title, item.mediaMetadata.title?.toString() ?: item.mediaId)
                    views.setOnClickFillInIntent(R.id.widget_item_root, Intent().putExtra("EXTRA_INDEX", position).putExtra("WIDGET_ACTION", "PLAYLIST_ITEM"))
                }
                "folders" -> {
                    views.setViewVisibility(R.id.widget_item_icon, android.view.View.GONE)
                    val folder = folders[position]
                    views.setTextViewText(R.id.widget_item_title, folder.name)
                    views.setOnClickFillInIntent(R.id.widget_item_root, Intent().putExtra("FOLDER_ID", folder.id).putExtra("WIDGET_ACTION", "OPEN_FOLDER"))
                }
                "folder_items", "search_results" -> {
                    views.setViewVisibility(R.id.widget_item_icon, android.view.View.GONE)
                    val file = folderItems[position]
                    views.setTextViewText(R.id.widget_item_title, file.name)
                    views.setOnClickFillInIntent(R.id.widget_item_root, Intent().putExtra("MEDIA_URI", file.uri.toString()).putExtra("WIDGET_ACTION", "PLAY_FILE"))
                }
            }
            return views
        } catch (e: Exception) {
            return RemoteViews(context.packageName, R.layout.widget_list_item)
        }
    }

    override fun getLoadingView(): RemoteViews? = null
    override fun getViewTypeCount(): Int = 1
    override fun getItemId(position: Int): Long = position.toLong()
    override fun hasStableIds(): Boolean = true
}
