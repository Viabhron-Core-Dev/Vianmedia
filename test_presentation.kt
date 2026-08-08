import androidx.media3.effect.Presentation

fun main() {
    println(Presentation.LAYOUT_SCALE_TO_FIT)
    println(Presentation.LAYOUT_SCALE_TO_FIT_WITH_CROP)
    val clazz = Presentation::class.java
    for (f in clazz.declaredFields) {
        if (f.name.startsWith("LAYOUT_")) {
            println(f.name)
        }
    }
}
