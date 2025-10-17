class Person(val name: String, val age: Int) {
    fun greet() {
        println("Hello, my name is $name and I'm $age years old")
    }
}

fun main() {
    val person = Person("Alice", 30)
    person.greet()
}
