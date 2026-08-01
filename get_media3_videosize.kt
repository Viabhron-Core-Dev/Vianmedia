import androidx.media3.common.VideoSize

fun checkVideoSize(size: VideoSize) {
    println(size.width)
    println(size.height)
    // Are there any other fields? Let's check using reflection.
}
