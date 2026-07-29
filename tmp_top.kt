     1	package com.example.service
     2	
     3	import androidx.media3.exoplayer.ExoPlayer
     4	import androidx.compose.runtime.getValue
     5	import androidx.compose.runtime.setValue
     6	import androidx.media3.session.MediaSession
     7	import androidx.media3.session.MediaSessionService
     8	import androidx.media3.common.MediaItem
     9	import androidx.media3.common.Player
    10	import com.google.common.util.concurrent.ListenableFuture
    11	import com.google.common.util.concurrent.Futures
    12	import android.os.Handler
    13	import android.os.Looper
    14	import kotlinx.coroutines.launch
    15	import kotlinx.coroutines.CoroutineScope
    16	import kotlinx.coroutines.Dispatchers
    17	import kotlinx.coroutines.SupervisorJob
    18	import kotlinx.coroutines.cancel
    19	import coil.Coil
    20	import coil.request.ImageRequest
    21	import android.graphics.drawable.Drawable
    22	import android.graphics.drawable.BitmapDrawable
    23	
    24	import android.annotation.SuppressLint
    25	import android.graphics.PixelFormat
    26	import android.view.Gravity
    27	import android.view.WindowManager
    28	import androidx.compose.ui.platform.ComposeView
    29	import androidx.lifecycle.Lifecycle
    30	import androidx.lifecycle.LifecycleOwner
    31	import androidx.lifecycle.LifecycleRegistry
    32	import androidx.lifecycle.ViewModelStore
    33	import androidx.lifecycle.ViewModelStoreOwner
    34	import androidx.lifecycle.setViewTreeLifecycleOwner
    35	import androidx.lifecycle.setViewTreeViewModelStoreOwner
    36	import androidx.savedstate.SavedStateRegistry
    37	import androidx.savedstate.SavedStateRegistryController
    38	import androidx.savedstate.SavedStateRegistryOwner
    39	import androidx.savedstate.setViewTreeSavedStateRegistryOwner
    40	
    41	class PlaybackService : MediaSessionService(), LifecycleOwner, ViewModelStoreOwner, SavedStateRegistryOwner {
    42	
    43	    private val lifecycleRegistry = LifecycleRegistry(this)
    44	    private val store = ViewModelStore()
    45	    private val savedStateRegistryController = SavedStateRegistryController.create(this)
    46	    private lateinit var windowManager: WindowManager
    47	    private var composeView: ComposeView? = null
    48	    private var layoutParams: WindowManager.LayoutParams? = null
    49	
    50	    override val lifecycle: Lifecycle get() = lifecycleRegistry
    51	    override val viewModelStore: ViewModelStore get() = store
    52	    override val savedStateRegistry: SavedStateRegistry get() = savedStateRegistryController.savedStateRegistry
    53	
    54	    private var mediaSession: MediaSession? = null
    55	    private val serviceScope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    56	
    57	    // Removed inactivity timeout
    58	
    59	    override fun onCreate() {
    60	        super.onCreate()
    61	        savedStateRegistryController.performRestore(null)
    62	        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_CREATE)
    63	        windowManager = getSystemService(android.content.Context.WINDOW_SERVICE) as WindowManager
    64	        
    65	        try {
    66	            val defaultProvider = androidx.media3.session.DefaultMediaNotificationProvider(this).apply {
    67	                // Media3 DefaultMediaNotificationProvider automatically adds custom layout commands
    68	            }
    69	            setMediaNotificationProvider(defaultProvider)
    70	        } catch (e: Exception) {
    71	            com.example.LogKeeper.logError("PlaybackService", "Failed to set up MediaNotificationProvider", e)
    72	        }
    73	        
    74	        val settings = com.example.data.SettingsManager.getInstance(this)
    75	        PlayerManager.initialize(this, false)
    76	        
    77	        val filter = android.content.IntentFilter("com.example.ACTION_WIDGET_COMMAND")
    78	        filter.addAction("com.example.ACTION_UPDATE_NOTIFICATION")
    79	        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
    80	            registerReceiver(widgetCommandReceiver, filter, android.content.Context.RECEIVER_NOT_EXPORTED)
    81	        } else {
    82	            registerReceiver(widgetCommandReceiver, filter)
    83	        }
    84	
    85	        PlayerManager.exoPlayer?.addListener(object : Player.Listener {
    86	            override fun onIsPlayingChanged(isPlaying: Boolean) { updateWidgetUI() }
    87	            override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) { updateWidgetUI() }
    88	            override fun onRepeatModeChanged(repeatMode: Int) { updateWidgetUI() }
    89	            override fun onShuffleModeEnabledChanged(shuffleModeEnabled: Boolean) { updateWidgetUI() }
    90	            override fun onTimelineChanged(timeline: androidx.media3.common.Timeline, reason: Int) { updateWidgetUI() }
    91	            override fun onPlayerError(error: androidx.media3.common.PlaybackException) {
    92	                val cause = error.cause?.message ?: "Unknown"
    93	                com.example.LogKeeper.logError("PlaybackService", "Error: ${error.errorCodeName} - ${error.message} - Cause: $cause", error)
    94	            }
    95	            override fun onPlaybackStateChanged(playbackState: Int) {
    96	                val stateName = when (playbackState) {
    97	                    Player.STATE_IDLE -> "STATE_IDLE"
    98	                    Player.STATE_BUFFERING -> "STATE_BUFFERING"
    99	                    Player.STATE_READY -> "STATE_READY"
   100	                    Player.STATE_ENDED -> "STATE_ENDED"
   101	                    else -> "UNKNOWN"
   102	                }
   103	                com.example.LogKeeper.log("Playback state changed to: $stateName", "PlaybackService")
   104	                if (playbackState == Player.STATE_ENDED) {
   105	                    val player = PlayerManager.exoPlayer
   106	                    if (player?.repeatMode == Player.REPEAT_MODE_OFF) {
   107	                        stopSelf()
   108	                    }
   109	                } else if (playbackState == Player.STATE_IDLE) {
   110	                    val player = PlayerManager.exoPlayer
   111	                    if (player != null && player.mediaItemCount == 0) {
   112	                        stopSelf()
   113	                    }
   114	                }
   115	            }
   116	            override fun onPlayWhenReadyChanged(playWhenReady: Boolean, reason: Int) {
   117	                if (reason == Player.PLAY_WHEN_READY_CHANGE_REASON_END_OF_MEDIA_ITEM) {
   118	                    val player = PlayerManager.exoPlayer
   119	                    if (player?.repeatMode == Player.REPEAT_MODE_OFF) {
   120	                        player.stop()
   121	                        player.clearMediaItems()
   122	                        stopSelf()
   123	                    }
   124	                }
   125	            }
   126	        })
   127	        
   128	
   129	        val intent = android.content.Intent(this, com.example.MainActivity::class.java).apply {
   130	            action = "com.example.ACTION_OPEN_PLAYER"
   131	        }
   132	        val pendingIntent = android.app.PendingIntent.getActivity(
   133	            this, 0, intent,
   134	            android.app.PendingIntent.FLAG_IMMUTABLE or android.app.PendingIntent.FLAG_UPDATE_CURRENT
   135	        )
   136	        mediaSession = MediaSession.Builder(this, PlayerManager.exoPlayer!!)
   137	            .setSessionActivity(pendingIntent)
   138	            .setBitmapLoader(com.example.MyBitmapLoader(this))
   139	            .setCallback(object : MediaSession.Callback {
   140	                override fun onConnect(
   141	                    session: MediaSession,
   142	                    controller: MediaSession.ControllerInfo
   143	                ): MediaSession.ConnectionResult {
   144	                    val defaultResult = super.onConnect(session, controller)
   145	                    val customCommands = defaultResult.availableSessionCommands.buildUpon()
   146	                        .add(androidx.media3.session.SessionCommand("ADD_SUBTITLE", android.os.Bundle.EMPTY))
   147	                        .add(androidx.media3.session.SessionCommand("SET_BOOST_GAIN", android.os.Bundle.EMPTY))
   148	                        .add(androidx.media3.session.SessionCommand("ACTION_CLOSE", android.os.Bundle.EMPTY))
   149	                        .add(androidx.media3.session.SessionCommand("ACTION_MORE", android.os.Bundle.EMPTY))
   150	                        .add(androidx.media3.session.SessionCommand("ACTION_LESS", android.os.Bundle.EMPTY))
   151	                        .add(androidx.media3.session.SessionCommand("ACTION_LOOP", android.os.Bundle.EMPTY))
   152	                        .add(androidx.media3.session.SessionCommand("ACTION_OVERLAY", android.os.Bundle.EMPTY))
   153	                        .add(androidx.media3.session.SessionCommand("ACTION_PIP", android.os.Bundle.EMPTY))
   154	                        .build()
   155	                    return MediaSession.ConnectionResult.accept(customCommands, defaultResult.availablePlayerCommands)
   156	                }
   157	
   158	                override fun onCustomCommand(
   159	                    session: MediaSession,
   160	                    controller: MediaSession.ControllerInfo,
   161	                    customCommand: androidx.media3.session.SessionCommand,
   162	                    args: android.os.Bundle
   163	                ): ListenableFuture<androidx.media3.session.SessionResult> {
   164	                    if (customCommand.customAction == "SET_BOOST_GAIN") {
   165	                        val gainMb = args.getInt("gainMb", 0)
   166	                        PlayerManager.setBoostGain(gainMb)
   167	                        return Futures.immediateFuture(androidx.media3.session.SessionResult(androidx.media3.session.SessionResult.RESULT_SUCCESS))
   168	                    }
   169	
   170	                    if (customCommand.customAction == "ACTION_CLOSE") {
   171	                        val player = session.player
   172	                        player.stop()
   173	                        player.clearMediaItems()
   174	                        stopSelf()
   175	                        return Futures.immediateFuture(androidx.media3.session.SessionResult(androidx.media3.session.SessionResult.RESULT_SUCCESS))
   176	                    }
   177	
   178	                    if (customCommand.customAction == "ACTION_LOOP") {
   179	                        val player = session.player
   180	                        player.repeatMode = when (player.repeatMode) {
   181	                            androidx.media3.common.Player.REPEAT_MODE_OFF -> androidx.media3.common.Player.REPEAT_MODE_ALL
   182	                            androidx.media3.common.Player.REPEAT_MODE_ALL -> androidx.media3.common.Player.REPEAT_MODE_ONE
   183	                            else -> androidx.media3.common.Player.REPEAT_MODE_OFF
   184	                        }
   185	                        updateCustomLayout()
   186	                        return Futures.immediateFuture(androidx.media3.session.SessionResult(androidx.media3.session.SessionResult.RESULT_SUCCESS))
   187	                    }
   188	                    if (customCommand.customAction == "ACTION_OVERLAY") {
   189	                        if (!android.provider.Settings.canDrawOverlays(this@PlaybackService)) {
   190	                            val intent = android.content.Intent(android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION, android.net.Uri.parse("package:$packageName"))
   191	                            intent.addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
   192	                            startActivity(intent)
   193	                        } else {
   194	                            if (composeView == null) {
   195	                                showOverlay()
   196	                            } else {
   197	                                hideOverlay()
   198	                            }
   199	                        }
   200	                        return Futures.immediateFuture(androidx.media3.session.SessionResult(androidx.media3.session.SessionResult.RESULT_SUCCESS))
   201	                    }
   202	                    if (customCommand.customAction == "ACTION_PIP") {
   203	                        // Broadcast to MainActivity to enter PiP
   204	                        val intent = android.content.Intent("com.example.ACTION_ENTER_PIP")
   205	                        sendBroadcast(intent)
   206	                        return Futures.immediateFuture(androidx.media3.session.SessionResult(androidx.media3.session.SessionResult.RESULT_SUCCESS))
   207	                    }
   208	
   209	                    if (customCommand.customAction == "ADD_SUBTITLE") {
   210	                        val uriStr = args.getString("subtitle_uri")
   211	                        if (uriStr != null) {
   212	                            val player = session.player
   213	                            val currentItem = player.currentMediaItem
   214	                            if (currentItem != null) {
   215	                                val mimeType = if (uriStr.endsWith(".vtt", true)) androidx.media3.common.MimeTypes.TEXT_VTT
   216	                                    else if (uriStr.endsWith(".ssa", true) || uriStr.endsWith(".ass", true)) androidx.media3.common.MimeTypes.TEXT_SSA
   217	                                    else androidx.media3.common.MimeTypes.APPLICATION_SUBRIP
   218	
   219	                                val subtitleConfig = MediaItem.SubtitleConfiguration.Builder(android.net.Uri.parse(uriStr))
   220	                                    .setMimeType(mimeType)
   221	                                    .setLanguage(null)
   222	                                    .setSelectionFlags(androidx.media3.common.C.SELECTION_FLAG_DEFAULT)
   223	                                    .build()
   224	                                
   225	                                val newItemBuilder = currentItem.buildUpon()
   226	                                val oldConfigs = currentItem.localConfiguration?.subtitleConfigurations
   227	                                if (oldConfigs != null) {
   228	                                    newItemBuilder.setSubtitleConfigurations(oldConfigs + subtitleConfig)
   229	                                } else {
   230	                                    newItemBuilder.setSubtitleConfigurations(listOf(subtitleConfig))
   231	                                }
   232	                                
   233	                                val newItem = newItemBuilder.build()
   234	                                val currentItemIndex = player.currentMediaItemIndex
   235	                                player.replaceMediaItem(currentItemIndex, newItem)
   236	                                
   237	                                // Reset the track selection to enable text tracks
   238	                                val builder = player.trackSelectionParameters.buildUpon()
   239	                                builder.setTrackTypeDisabled(androidx.media3.common.C.TRACK_TYPE_TEXT, false)
   240	                                player.trackSelectionParameters = builder.build()
   241	                            }
   242	                        }
   243	                        return Futures.immediateFuture(androidx.media3.session.SessionResult(androidx.media3.session.SessionResult.RESULT_SUCCESS))
   244	                    }
   245	                    return super.onCustomCommand(session, controller, customCommand, args)
   246	                }
   247	
   248	                override fun onAddMediaItems(
   249	                    mediaSession: MediaSession,
   250	                    controller: MediaSession.ControllerInfo,
   251	                    mediaItems: List<MediaItem>
   252	                ): ListenableFuture<List<MediaItem>> {
   253	                    com.example.LogKeeper.log("onAddMediaItems called with ${mediaItems.size} items", "PlaybackService")
   254	                    val updatedMediaItems = mediaItems.map { mediaItem ->
   255	                        val uriToUse = mediaItem.localConfiguration?.uri?.toString() ?: mediaItem.mediaId
   256	                        com.example.LogKeeper.log("Transforming mediaItem to use URI: $uriToUse", "PlaybackService")
   257	                        mediaItem.buildUpon()
   258	                            .setUri(uriToUse)
   259	                            .build()
   260	                    }
   261	                    return Futures.immediateFuture(updatedMediaItems)
   262	                }
   263	            }).build()
   264	            
   265	        updateCustomLayout()
   266	        
   267	        addSession(mediaSession!!)
   268	    }
   269	
   270	    override fun onGetSession(controllerInfo: MediaSession.ControllerInfo): MediaSession? {
   271	        return mediaSession
   272	    }
   273	
   274	    override fun onTaskRemoved(rootIntent: android.content.Intent?) {
   275	        super.onTaskRemoved(rootIntent)
   276	        com.example.LogKeeper.log("onTaskRemoved called, cleaning up.", "PlaybackService")
   277	        val player = mediaSession?.player
   278	        if (player != null && (!player.playWhenReady || player.mediaItemCount == 0 || player.playbackState == androidx.media3.common.Player.STATE_ENDED)) {
   279	            player.stop()
   280	            stopSelf()
   281	        }
   282	    }
   283	
   284	
   285	    @SuppressLint("ClickableViewAccessibility")
   286	    private fun showOverlay() {
   287	        if (composeView != null) return
   288	        val cv = ComposeView(this)
   289	        composeView = cv
   290	        cv.setViewTreeLifecycleOwner(this@PlaybackService)
   291	        cv.setViewTreeViewModelStoreOwner(this@PlaybackService)
   292	        cv.setViewTreeSavedStateRegistryOwner(this@PlaybackService)
   293	        
   294	        val prefs = getSharedPreferences("MiniPlayerPrefs", android.content.Context.MODE_PRIVATE)
   295	
   296	        cv.setContent {
   297	            var isMinimized by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
   298	
   299	            com.example.ui.theme.MyApplicationTheme {
   300	                com.example.ui.components.MiniPlayerOverlay(
   301	                player = com.example.service.PlayerManager.exoPlayer,
   302	                onClose = {
   303	                    val player = com.example.service.PlayerManager.exoPlayer
   304	                    player?.stop()
   305	                    player?.clearMediaItems()
   306	                    hideOverlay()
   307	                    stopSelf()
   308	                },
   309	                onMinimize = {
   310	                    hideOverlay()
   311	                },
   312	                onDrag = { dx, dy ->
   313	                    val lp = layoutParams
   314	                    if (lp != null) {
   315	                        lp.x += dx.toInt()
   316	                        lp.y += dy.toInt()
   317	                        windowManager.updateViewLayout(cv, lp)
   318	                        prefs.edit().putInt("x", lp.x).putInt("y", lp.y).apply()
   319	                    }
   320	                },
   321	                onResize = { dw, dh ->
   322	                    val lp = layoutParams
   323	                    if (lp != null) {
   324	                        lp.width = (lp.width + dw.toInt()).coerceAtLeast(400)
   325	                        lp.height = (lp.height + dh.toInt()).coerceAtLeast(400)
   326	                        windowManager.updateViewLayout(cv, lp)
   327	                        prefs.edit().putInt("width", lp.width).putInt("height", lp.height).apply()
   328	                    }
   329	                },
   330	                isMinimizedExternal = isMinimized,
   331	                onMinimizeChange = { minimized ->
   332	                    isMinimized = minimized
   333	                    val lp = layoutParams
   334	                    if (lp != null) {
   335	                        if (minimized) {
   336	                            lp.width = WindowManager.LayoutParams.WRAP_CONTENT
   337	                            lp.height = WindowManager.LayoutParams.WRAP_CONTENT
   338	                        } else {
   339	                            val metrics = resources.displayMetrics
   340	                            lp.width = prefs.getInt("width", (300 * metrics.density).toInt())
   341	                            lp.height = prefs.getInt("height", (200 * metrics.density).toInt())
   342	                        }
   343	                        windowManager.updateViewLayout(cv, lp)
   344	                    }
   345	                }
   346	            )
   347	        }
   348	        val type = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
   349	            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
   350	        } else {
   351	            @Suppress("DEPRECATION")
   352	            WindowManager.LayoutParams.TYPE_PHONE
   353	        }
   354	        val metrics = resources.displayMetrics
   355	        val widthPx = prefs.getInt("width", (300 * metrics.density).toInt())
   356	        val heightPx = prefs.getInt("height", (200 * metrics.density).toInt())
   357	        layoutParams = WindowManager.LayoutParams(
   358	            widthPx,
   359	            heightPx,
   360	            type,
   361	            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
   362	            PixelFormat.TRANSLUCENT
   363	        ).apply {
   364	            gravity = Gravity.TOP or Gravity.START
   365	            x = prefs.getInt("x", 100)
   366	            y = prefs.getInt("y", 100)
   367	        }
   368	        windowManager.addView(composeView, layoutParams)
   369	        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_START)
   370	        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_RESUME)
   371	    }
   372	
   373	    private fun hideOverlay() {
   374	        composeView?.let {
   375	            lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_PAUSE)
   376	            lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_STOP)
   377	            windowManager.removeView(it)
   378	        }
   379	        composeView = null
   380	    }
   381	
