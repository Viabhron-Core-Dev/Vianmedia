import re

with open("app/src/main/java/com/example/service/PlayerManager.kt", "r") as f:
    content = f.read()

import_statement = "import android.media.audiofx.LoudnessEnhancer"
new_imports = """import android.media.audiofx.LoudnessEnhancer
import android.media.audiofx.Equalizer
import android.media.audiofx.DynamicsProcessing
import android.os.Build"""

content = content.replace(import_statement, new_imports)

vars_old = """    var exoPlayer: ExoPlayer? = null
    var loudnessEnhancer: LoudnessEnhancer? = null"""
vars_new = """    var exoPlayer: ExoPlayer? = null
    var loudnessEnhancer: LoudnessEnhancer? = null
    var equalizer: Equalizer? = null
    var dynamicsProcessing: DynamicsProcessing? = null
    val centerChannelProcessor = CenterChannelAudioProcessor()"""

content = content.replace(vars_old, vars_new)

renderers_old = """        val renderersFactory = androidx.media3.exoplayer.DefaultRenderersFactory(context.applicationContext)
            .setEnableDecoderFallback(true)
            .setExtensionRendererMode(
                when (settings.decoderPriority) {
                    0 -> androidx.media3.exoplayer.DefaultRenderersFactory.EXTENSION_RENDERER_MODE_OFF
                    1 -> androidx.media3.exoplayer.DefaultRenderersFactory.EXTENSION_RENDERER_MODE_ON
                    2 -> androidx.media3.exoplayer.DefaultRenderersFactory.EXTENSION_RENDERER_MODE_PREFER
                    else -> androidx.media3.exoplayer.DefaultRenderersFactory.EXTENSION_RENDERER_MODE_ON
                }
            )"""

renderers_new = """        val renderersFactory = object : androidx.media3.exoplayer.DefaultRenderersFactory(context.applicationContext) {
            override fun buildAudioSink(
                context: android.content.Context,
                enableFloatOutput: Boolean,
                enableAudioTrackPlaybackParams: Boolean
            ): androidx.media3.exoplayer.audio.AudioSink? {
                return androidx.media3.exoplayer.audio.DefaultAudioSink.Builder(context)
                    .setAudioProcessors(arrayOf(centerChannelProcessor))
                    .setEnableFloatOutput(enableFloatOutput)
                    .setEnableAudioTrackPlaybackParams(enableAudioTrackPlaybackParams)
                    .build()
            }
        }.setEnableDecoderFallback(true)
            .setExtensionRendererMode(
                when (settings.decoderPriority) {
                    0 -> androidx.media3.exoplayer.DefaultRenderersFactory.EXTENSION_RENDERER_MODE_OFF
                    1 -> androidx.media3.exoplayer.DefaultRenderersFactory.EXTENSION_RENDERER_MODE_ON
                    2 -> androidx.media3.exoplayer.DefaultRenderersFactory.EXTENSION_RENDERER_MODE_PREFER
                    else -> androidx.media3.exoplayer.DefaultRenderersFactory.EXTENSION_RENDERER_MODE_ON
                }
            )"""

content = content.replace(renderers_old, renderers_new)

session_old = """            override fun onAudioSessionIdChanged(audioSessionId: Int) {
                if (audioSessionId != C.AUDIO_SESSION_ID_UNSET) {
                    try {
                        loudnessEnhancer?.release()
                        loudnessEnhancer = LoudnessEnhancer(audioSessionId)
                        val settings = com.example.data.SettingsManager.getInstance(context.applicationContext)
                        if (settings.audioBoosterEnabled && settings.boostGainMb > 0) {
                            loudnessEnhancer?.setTargetGain(settings.boostGainMb)
                            loudnessEnhancer?.enabled = true
                        } else {
                            loudnessEnhancer?.enabled = false
                        }
                    } catch (e: Exception) {
                        com.example.LogKeeper.logError("PlayerManager", "Failed to create LoudnessEnhancer on session change", e)
                    }
                }
            }"""

session_new = """            override fun onAudioSessionIdChanged(audioSessionId: Int) {
                if (audioSessionId != C.AUDIO_SESSION_ID_UNSET) {
                    try {
                        loudnessEnhancer?.release()
                        loudnessEnhancer = LoudnessEnhancer(audioSessionId)
                        
                        equalizer?.release()
                        try { equalizer = Equalizer(0, audioSessionId) } catch (e: Exception) {}
                        
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                            dynamicsProcessing?.release()
                            try {
                                val config = DynamicsProcessing.Config.Builder(
                                    DynamicsProcessing.VARIANT_FAVOR_FREQUENCY_RESOLUTION,
                                    2, true, 0, true, 0, true, 0, true
                                )
                                .build()
                                dynamicsProcessing = DynamicsProcessing(0, audioSessionId, config)
                            } catch (e: Exception) {}
                        }
                        
                        val settings = com.example.data.SettingsManager.getInstance(context.applicationContext)
                        
                        if (settings.audioBoosterEnabled && settings.boostGainMb > 0) {
                            loudnessEnhancer?.setTargetGain(settings.boostGainMb)
                            loudnessEnhancer?.enabled = true
                        } else {
                            loudnessEnhancer?.enabled = false
                        }
                        
                        applyAudioEffects(settings)
                        
                    } catch (e: Exception) {
                        com.example.LogKeeper.logError("PlayerManager", "Failed to create AudioEffects on session change", e)
                    }
                }
            }"""

content = content.replace(session_old, session_new)

apply_audio_effects = """
    fun applyAudioEffects(settings: com.example.data.SettingsManager) {
        centerChannelProcessor.enabled = settings.centerChannelEnabled
        
        try {
            equalizer?.let { eq ->
                eq.enabled = settings.eqEnabled
                if (settings.eqEnabled) {
                    val levels = settings.getEqLevels()
                    if (levels.isNotEmpty() && levels.size == eq.numberOfBands.toInt()) {
                        for (i in 0 until eq.numberOfBands) {
                            eq.setBandLevel(i.toShort(), levels[i].toShort())
                        }
                    }
                }
            }
            
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                dynamicsProcessing?.let { dp ->
                    dp.enabled = settings.nightModeEnabled
                    if (settings.nightModeEnabled) {
                        // Very aggressive compression for night mode / loudness leveling
                        val mbc = DynamicsProcessing.Mbc(true, true, 1)
                        val mbcBand = DynamicsProcessing.MbcBand(true, 1000f, -40f, 10f, -50f, 4f, -40f, 4f)
                        mbc.setBand(0, mbcBand)
                        dp.setMbcAllChannelsTo(mbc)
                    }
                }
            }
        } catch (e: Exception) {
            com.example.LogKeeper.logError("PlayerManager", "Error applying audio effects", e)
        }
    }
"""

content = content.replace("fun setBoostGain(gainMb: Int) {", apply_audio_effects + "\n    fun setBoostGain(gainMb: Int) {")

release_old = """    fun release() {
        exoPlayer?.release()
        exoPlayer = null
        loudnessEnhancer?.release()
        loudnessEnhancer = null
    }"""
release_new = """    fun release() {
        exoPlayer?.release()
        exoPlayer = null
        loudnessEnhancer?.release()
        loudnessEnhancer = null
        equalizer?.release()
        equalizer = null
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            dynamicsProcessing?.release()
        }
        dynamicsProcessing = null
    }"""
content = content.replace(release_old, release_new)

with open("app/src/main/java/com/example/service/PlayerManager.kt", "w") as f:
    f.write(content)
