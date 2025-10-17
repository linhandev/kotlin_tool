
data class Person(val name: String, val age: Int, val city: String)

fun main() {
    val people = listOf(
        Person("Alice", 30, "NYC"),
        Person("Bob", 25, "LA"),
        Person("Charlie", 35, "NYC"),
        Person("David", 28, "LA")
    )
    
    val byCity = people.groupBy { it.city }
    println("By city: $byCity")
    
    val avgAge = people.map { it.age }.average()
    println("Average age: $avgAge")
    
    val names = people.associate { it.name to it.age }
    println("Names to ages: $names")
}
