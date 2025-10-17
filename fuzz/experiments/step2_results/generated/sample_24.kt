
interface Node<T: Node<T>> {
    fun getSelf(): T
}

class TreeNode(val value: Int) : Node<TreeNode> {
    override fun getSelf(): TreeNode = this
}

fun <T: Node<T>> processNode(node: T): T {
    return node.getSelf()
}

fun main() {
    val node = TreeNode(42)
    val processed = processNode(node)
    println("Node value: ${processed.value}")
}
