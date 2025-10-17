fun main() {
    val numbers = listOf(1, 2, 3, 4, 5)
    val doubled = numbers.map { it * 2 }
    println("Doubled: $doubled")
    
    val evens = numbers.filter { it % 2 == 0 }
    println("Evens: $evens")
}
