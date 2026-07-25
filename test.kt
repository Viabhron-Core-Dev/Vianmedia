fun test(name: String) = name.substringBeforeLast('.')
fun main() {
    println(test("123"))
    println(test("video.mp4"))
}
