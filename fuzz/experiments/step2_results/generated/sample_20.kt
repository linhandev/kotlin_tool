
abstract class Animal(val name: String) {
    abstract fun makeSound(): String
    open fun describe(): String = "Animal: $name"
}

interface Flyable {
    fun fly(): String
}

interface Swimmable {
    fun swim(): String
}

open class Bird(name: String) : Animal(name), Flyable {
    override fun makeSound() = "Tweet"
    override fun fly() = "$name is flying"
}

class Duck(name: String) : Bird(name), Swimmable {
    override fun makeSound() = "Quack"
    override fun swim() = "$name is swimming"
}

fun main() {
    val duck = Duck("Donald")
    println(duck.describe())
    println(duck.makeSound())
    println(duck.fly())
    println(duck.swim())
}
