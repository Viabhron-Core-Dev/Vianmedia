import androidx.media3.common.VideoSize
fun main() {
    val methods = VideoSize::class.java.methods
    val fields = VideoSize::class.java.fields
    for (m in methods) println(m.name)
    for (f in fields) println(f.name)
}
