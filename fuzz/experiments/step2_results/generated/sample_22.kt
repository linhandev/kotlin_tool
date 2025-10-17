
data class Box<T>(val value: T) {
    operator fun plus(other: Box<T>): String {
        return "${this.value} + ${other.value}"
    }
}

operator fun <T> Box<T>.times(count: Int): List<T> {
    return List(count) { value }
}

fun main() {
    val box1 = Box(10)
    val box2 = Box(20)
    
    println(box1 + box2)
    println(box1 * 3)
}
