infix fun Int.pow(exponent: Int): Int {
    var result = 1
    repeat(exponent) {
        result *= this
    }
    return result
}

fun main() {
    val result = 2 pow 3
    println("2 pow 3 = $result")
}
