
interface Mapper<A, B, C, D> {
    fun map(a: A, b: B, c: C): D
}

class QuadMapper<T1, T2, T3, T4> : Mapper<T1, T2, T3, T4> where T1: Number, T2: Number, T3: Number {
    override fun map(a: T1, b: T2, c: T3): T4 {
        @Suppress("UNCHECKED_CAST")
        return (a.toInt() + b.toInt() + c.toInt()) as T4
    }
}

fun <A, B, C, D, E> transform(a: A, b: B, c: C, f: (A, B, C) -> D, g: (D) -> E): E {
    return g(f(a, b, c))
}

fun main() {
    val mapper = QuadMapper<Int, Double, Long, Int>()
    val result = mapper.map(1, 2.0, 3L)
    println("Mapped: $result")
    
    val transformed = transform(1, 2, 3, 
        { x, y, z -> x + y + z },
        { it * 2 }
    )
    println("Transformed: $transformed")
}
