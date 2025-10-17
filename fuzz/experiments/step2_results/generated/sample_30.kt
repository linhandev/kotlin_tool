
interface Comparable<T> {
    fun compareTo(other: T): Int
}

class GenericHolder<T: Any>(val value: T) {
    fun get(): T = value
    fun set(newValue: T): T {
        return newValue
    }
}

fun main() {
    val intHolder = GenericHolder<Int>(42)
    println("Value: ${intHolder.get()}")
    
    val stringHolder = GenericHolder("Hello")
    println("String: ${stringHolder.get()}")
}
