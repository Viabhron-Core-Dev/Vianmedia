package com.example
import androidx.media3.effect.Presentation
class TestPresentation {
    fun test() {
        val presentation = Presentation.createForAspectRatio(16f / 9f, Presentation.LAYOUT_SCALE_TO_FIT)
    }
}
