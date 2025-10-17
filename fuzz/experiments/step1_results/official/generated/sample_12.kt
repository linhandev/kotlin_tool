class Example {
    var p: String by lazy {
        println("Computing value")
        "Lazy value"
    }
}

fun main() {
    val example = Example()
    println("Before accessing")
    println(example.p)
    println(example.p)
}
