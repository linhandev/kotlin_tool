fun <T> printList(items: List<T>) {
    for (item in items) {
        println(item)
    }
}

fun main() {
    printList(listOf(1, 2, 3))
    printList(listOf("a", "b", "c"))
}
