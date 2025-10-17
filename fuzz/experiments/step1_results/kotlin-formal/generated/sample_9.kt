class Counter {
    companion object {
        var count = 0
        fun increment() {
            count++
        }
    }
}

fun main() {
    Counter.increment()
    Counter.increment()
    println("Count: ${Counter.count}")
}
