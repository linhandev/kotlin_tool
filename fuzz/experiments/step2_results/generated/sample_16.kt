
fun <T, R> List<T>.customMap(transform: (T) -> R): List<R> {
    val result = mutableListOf<R>()
    for (item in this) {
        result.add(transform(item))
    }
    return result
}

fun <T> List<T>.customFilter(predicate: (T) -> Boolean): List<T> {
    val result = mutableListOf<T>()
    for (item in this) {
        if (predicate(item)) {
            result.add(item)
        }
    }
    return result
}

fun main() {
    val numbers = listOf(1, 2, 3, 4, 5)
    val doubled = numbers.customMap { it * 2 }
    val evens = numbers.customFilter { it % 2 == 0 }
    
    println("Doubled: $doubled")
    println("Evens: $evens")
}
