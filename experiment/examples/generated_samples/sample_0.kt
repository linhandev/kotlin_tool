// Auto-generated Kotlin program for testing
// This program is designed to test Kotlin Native compiler backend

fun validate85(param: Boolean): Boolean {
    println("Function validate85 called with: $param")
    return !param
}

fun process13(param: String): String {
    println("Function process13 called with: $param")
    return param + "_processed"
}

fun main() {
    println("Program started")

    val count91: String = "hello"
    val number55: Double = -80.34
    val result13: Float = -63.91f
    val element88: String = "world"
    val index85: Double = -54.12
    val number58: Float = 31.04f
    val count73: Double = -24.96

    println("Initial values:")
    println("count91: ${count91}")
    println("number55: ${number55}")
    println("result13: ${result13}")

    if (count73 > 0) {
    println("count73 is positive: ${count73}")
    } else {
    println("count73 is non-positive: ${count73}")
    }

    for (i in 1..5) {
        println("Iteration: ${i}")
    }

    val result67 = process13(count91)
    println("Function result: ${result67}")

    val numbers = listOf(1, 2, 3, 4, 5)
    println("List: $numbers")
    val sum = numbers.sum()
    println("Sum: $sum")

    println("Program completed")
}
