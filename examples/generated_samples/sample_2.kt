// Auto-generated Kotlin program for testing
// This program is designed to test Kotlin Native compiler backend

fun process48(param: String): String {
    println("Function process48 called with: $param")
    return param + "_processed"
}

fun process64(param: Boolean): Boolean {
    println("Function process64 called with: $param")
    return !param
}

fun main() {
    println("Program started")

    val value38: Boolean = true
    val text24: Int = -779
    val item85: Long = 494L
    val flag10: Int = 418
    val element62: Long = 527L
    val number53: Int = 786

    println("Initial values:")
    println("value38: ${value38}")
    println("text24: ${text24}")
    println("item85: ${item85}")

    if (item85 > 0) {
    println("item85 is positive: ${item85}")
    } else {
    println("item85 is non-positive: ${item85}")
    }

    for (i in 1..3) {
        println("Iteration: ${i}")
    }

    when {
        text24 > 0 -> println("text24 is positive")
        text24 < 0 -> println("text24 is negative")
        else -> println("text24 is zero")
    }

    val result66 = process64(value38)
    println("Function result: ${result66}")

    val numbers = listOf(1, 2, 3, 4, 5)
    println("List: $numbers")
    val sum = numbers.sum()
    println("Sum: $sum")

    println("Program completed")
}
