
fun <T, R, S> curry(f: (T, R) -> S): (T) -> (R) -> S {
    return { t -> { r -> f(t, r) } }
}

fun add(a: Int, b: Int): Int = a + b

fun main() {
    val curriedAdd = curry(::add)
    val add5 = curriedAdd(5)
    
    println("5 + 3 = ${add5(3)}")
    println("5 + 7 = ${add5(7)}")
}
