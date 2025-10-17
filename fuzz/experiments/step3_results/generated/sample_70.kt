
class Level1 {
    class Level2 {
        class Level3 {
            class Level4 {
                val value = "Nested"
            }
        }
    }
}

fun process(): String {
    val l1 = Level1()
    val l2 = Level1.Level2()
    val l3 = Level1.Level2.Level3()
    val l4 = Level1.Level2.Level3.Level4()
    return l4.value
}

fun main() {
    println("Result: ${process()}")
    
    val nested = listOf(1, 2, 3).map { a ->
        listOf(4, 5, 6).map { b ->
            listOf(7, 8, 9).filter { c ->
                (a + b + c) % 2 == 0
            }.map { c -> a * b * c }
        }.flatten()
    }.flatten()
    
    println("Nested: ${nested.take(5)}")
}
