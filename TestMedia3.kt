import androidx.media3.common.VideoSize
import java.lang.reflect.Modifier

fun main() {
    val clazz = VideoSize::class.java
    for (f in clazz.fields) {
        println("Field: ${f.name} type=${f.type.name} deprecated=${f.isAnnotationPresent(java.lang.Deprecated::class.java)}")
    }
}
