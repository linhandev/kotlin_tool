
class Task<T>(val name: String, val compute: () -> T) {
    fun execute(): T {
        println("Executing task: $name")
        return compute()
    }
}

fun <T, R> Task<T>.map(transform: (T) -> R): Task<R> {
    return Task("${this.name}.map") {
        transform(this.execute())
    }
}

fun main() {
    val task1 = Task("fetch data") { 42 }
    val task2 = task1.map { it * 2 }
    val task3 = task2.map { "Result: $it" }
    
    println(task3.execute())
}
