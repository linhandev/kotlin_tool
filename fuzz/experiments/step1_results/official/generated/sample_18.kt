data class Vector(val x: Int, val y: Int) {
    operator fun plus(other: Vector) = Vector(x + other.x, y + other.y)
    operator fun times(scalar: Int) = Vector(x * scalar, y * scalar)
}

fun main() {
    val v1 = Vector(1, 2)
    val v2 = Vector(3, 4)
    val v3 = v1 + v2
    val v4 = v1 * 2
    
    println("v1 + v2 = $v3")
    println("v1 * 2 = $v4")
}
