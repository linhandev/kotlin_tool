fun String.addExclamation(): String {
    return this + "!"
}

fun Int.isEven(): Boolean = this % 2 == 0

fun main() {
    println("Hello".addExclamation())
    println("5 is even: ${5.isEven()}")
    println("4 is even: ${4.isEven()}")
}
