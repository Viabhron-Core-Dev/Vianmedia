package com.example
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.effect.ScaleAndRotateTransformation
import androidx.media3.effect.Crop
class TestSetEffects {
    fun test(player: ExoPlayer) {
        val rotate = ScaleAndRotateTransformation.Builder().setRotationDegrees(90f).build()
        player.setVideoEffects(listOf(rotate))
    }
}
