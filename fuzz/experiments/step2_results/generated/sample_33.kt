
interface Base {
    fun print()
    val value: String
}

class BaseImpl(val x: Int) : Base {
    override fun print() {
        println("BaseImpl: $x")
    }
    override val value: String = "Base value: $x"
}

class Derived(b: Base) : Base by b {
    override fun print() {
        println("Derived delegates to:")
        (this as? Base)?.let { }
    }
}

fun main() {
    val base = BaseImpl(10)
    val derived = Derived(base)
    base.print()
    println(base.value)
}
