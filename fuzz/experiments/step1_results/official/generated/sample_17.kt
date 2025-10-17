data class Point(val x: Int, val y: Int)

fun main() {
    val point = Point(10, 20)
    val (x, y) = point
    println("x = $x, y = $y")
    
    val map = mapOf(1 to "one", 2 to "two")
    for ((key, value) in map) {
        println("$key -> $value")
    }
}
