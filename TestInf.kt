fun main() {
    val aspect = 426f / 0f
    val validAspect = aspect.coerceIn(10000f/23900f, 23900f/10000f)
    println((validAspect * 10000).toInt())
}
