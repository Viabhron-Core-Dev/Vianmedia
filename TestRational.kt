fun main() {
    val width = 426
    val height = 240
    val aspect = width.toFloat() / height.toFloat()
    val validAspect = aspect.coerceIn(10000f/23900f, 23900f/10000f)
    println((validAspect * 10000).toInt())
    println(10000)
}
