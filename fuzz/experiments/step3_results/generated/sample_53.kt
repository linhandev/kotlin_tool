
typealias Transform<T> = (T) -> T

fun <T> chain(vararg transforms: Transform<T>): Transform<T> {
    return { value ->
        transforms.fold(value) { acc, transform -> transform(acc) }
    }
}

fun <T> repeat(n: Int, transform: Transform<T>): Transform<T> {
    return { value ->
        (0 until n).fold(value) { acc, _ -> transform(acc) }
    }
}

fun main() {
    val double: Transform<Int> = { it * 2 }
    val addOne: Transform<Int> = { it + 1 }
    val square: Transform<Int> = { it * it }
    
    val complex = chain(double, addOne, square)
    println("Complex(5): ${complex(5)}")
    
    val repeated = repeat(3, double)
    println("Repeated(5): ${repeated(5)}")
    
    val nested = listOf(1, 2, 3).map { a ->
        listOf(4, 5, 6).flatMap { b ->
            listOf(7, 8, 9).map { c ->
                a to (b to c)
            }.filter { (x, pair) ->
                val (y, z) = pair
                x + y + z > 10
            }
        }
    }.flatten()
    
    println("Nested: ${nested.size} items")
}
