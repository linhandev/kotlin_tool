
interface Container<out T> {
    fun get(): T
}

interface MutableContainer<T> : Container<T> {
    fun set(value: T)
}

class Box<T>(private var value: T) : MutableContainer<T> {
    override fun get(): T = value
    override fun set(value: T) { this.value = value }
}

fun <T> copyContainer(from: Container<T>, to: MutableContainer<T>) {
    to.set(from.get())
}

class Pair<out A, out B>(val first: A, val second: B)

fun <T> makePair(value: T): Pair<T, T> = Pair(value, value)

fun <A, B, C> mapPair(pair: Pair<A, B>, f: (A) -> C, g: (B) -> C): Pair<C, C> {
    return Pair(f(pair.first), g(pair.second))
}

fun main() {
    val box1 = Box(10)
    val box2 = Box(20)
    
    copyContainer(box1, box2)
    println("Box2 value: ${box2.get()}")
    
    val pair = makePair("hello")
    println("Pair: ${pair.first}, ${pair.second}")
    
    val intPair = Pair(1, 2)
    val mapped = mapPair(intPair, { it * 2 }, { it * 3 })
    println("Mapped: ${mapped.first}, ${mapped.second}")
}
