fun main() {
    try {
        Class.forName("androidx.media3.effect.DefaultVideoFrameProcessor")
        println("Found DefaultVideoFrameProcessor")
    } catch (e: Exception) {
        println("Not Found DefaultVideoFrameProcessor")
    }
}
