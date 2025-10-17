
interface A { fun funcA(): String = "A" }
interface B { fun funcB(): String = "B" }
interface C { fun funcC(): String = "C" }

abstract class BaseX : A, B {
    abstract fun process(): String
}

open class MiddleY : BaseX(), C {
    override fun process(): String = "Middle"
}

class FinalZ : MiddleY() {
    override fun process(): String = "Final"
    fun combined(): String = funcA() + funcB() + funcC() + process()
}

sealed class Tree<out T> {
    data class Leaf<T>(val value: T) : Tree<T>()
    data class Node<T>(val left: Tree<T>, val right: Tree<T>) : Tree<T>()
    object Empty : Tree<Nothing>()
}

fun <T> Tree<T>.depth(): Int = when (this) {
    is Tree.Leaf -> 1
    is Tree.Node -> 1 + maxOf(left.depth(), right.depth())
    Tree.Empty -> 0
}

fun main() {
    val obj = FinalZ()
    println("Combined: ${obj.combined()}")
    
    val tree = Tree.Node(
        Tree.Leaf(1),
        Tree.Node(Tree.Leaf(2), Tree.Leaf(3))
    )
    println("Tree depth: ${tree.depth()}")
}
