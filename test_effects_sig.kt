import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.common.Effect

fun test(player: ExoPlayer) {
    val effects = listOf<Effect>()
    player.setVideoEffects(effects)
}
