// Auto-generated diverse Kotlin program
// Testing Kotlin Native compiler backend
import kotlin.random.Random

// Feature: data_class
data class Data558(val prop0: String, val prop1: String, val prop2: Double)

// Feature: property_delegation
class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

// Feature: vararg
fun vararg611(vararg items: Int): Int = items.sum()

// Feature: destructuring
fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

// Feature: generics
class Gen992<T>(val value: T) {
    fun get(): T = value
    fun <R> map(fn: (T) -> R): Gen992<R> = Gen992(fn(value))
}

// Feature: ranges
val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

// Feature: lambda
val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

// Feature: enum_class
enum class Enum345 { VALUE0, VALUE1, VALUE2, VALUE3 }

// Feature: tailrec
tailrec fun tailrec753(n: Int, acc: Int = 1): Int {
    if (n <= 1) return acc
    return tailrec753(n - 1, acc * n)
}

// Feature: default_parameters
fun default720(x: Int = 10, y: String = "default"): String = "x=$x, y=$y"

// Feature: nested_class
class Outer416 {
    class Nested {
        fun doSomething() = 123
    }
}

// Feature: when_expression
val when697 = when (Random.nextInt(0, 5)) {
    0 -> "zero"
    1, 2 -> "one or two"
    in 3..4 -> "three or four"
    else -> "other"
}

// Feature: type_alias
typealias TypeAlias96 = Map<String, List<Int>>

// Feature: sealed_class
sealed class Sealed545 {
    object Sub0 : Sealed545()
    object Sub1 : Sealed545()
}

// Feature: infix_function
infix fun Int.infix892(other: Int): Int = this + other

// Feature: inline_function
inline fun inline418(block: () -> Unit) { block() }

// Feature: extension_function
fun List<Int>.ext233(): Int = this.sum()

// Feature: sequences
val seq = generateSequence(1) { if (it < 100) it * 2 else null }
val seqList = seq.take(5).toList()

fun main() {
    println("Program started - testing diverse Kotlin features")
    val obj1 = Data558(79, "c")
    println("Data class: $obj1")
    println("Vararg: ${vararg611(1, 2, 3)}")
    val numbers = listOf(1, 2, 3, 4, 5)
    println("Sum: ${numbers.sum()}")
    println("Filtered: ${numbers.filter { it > 2 }}")
    
    val range = 1..5
    for (i in range) {
        println("Iteration: $i")
    }
    
    println("Program completed")
}
