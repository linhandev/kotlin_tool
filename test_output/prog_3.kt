// Auto-generated diverse Kotlin program
// Testing Kotlin Native compiler backend
import kotlin.random.Random

// Feature: sealed_class
sealed class Sealed522 {
    object Sub0 : Sealed522()
    object Sub1 : Sealed522()
}

// Feature: when_expression
val when99 = when (Random.nextInt(0, 5)) {
    0 -> "zero"
    1, 2 -> "one or two"
    in 3..4 -> "three or four"
    else -> "other"
}

// Feature: tailrec
tailrec fun tailrec799(n: Int, acc: Int = 1): Int {
    if (n <= 1) return acc
    return tailrec799(n - 1, acc * n)
}

// Feature: ranges
val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

// Feature: infix_function
infix fun Int.infix844(other: Int): Int = this + other

// Feature: lambda
val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

// Feature: companion_object
class Comp845 {
    companion object {
        const val CONST_VAL = 42
        fun create(): Comp845 = Comp845()
    }
}

// Feature: default_parameters
fun default277(x: Int = 10, y: String = "default"): String = "x=$x, y=$y"

// Feature: generics
class Gen707<T>(val value: T) {
    fun get(): T = value
    fun <R> map(fn: (T) -> R): Gen707<R> = Gen707(fn(value))
}

// Feature: enum_class
enum class Enum853 { VALUE0, VALUE1, VALUE2, VALUE3 }

// Feature: inline_function
inline fun inline845(block: () -> Unit) { block() }

// Feature: sequences
val seq = generateSequence(1) { if (it < 100) it * 2 else null }
val seqList = seq.take(5).toList()

// Feature: extension_function
fun String.ext259(): String = this.uppercase()

// Feature: property_delegation
class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

// Feature: operator_overload
data class Op509(val value: Int) {
    operator fun plus(other: Op509): Op509 = Op509(value + other.value)
    operator fun times(factor: Int): Op509 = Op509(value * factor)
}

// Feature: destructuring
fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

// Feature: nested_class
class Outer73 {
    class Nested {
        fun doSomething() = 123
    }
}

// Feature: type_alias
typealias TypeAlias786 = Map<String, List<Int>>

fun main() {
    println("Program started - testing diverse Kotlin features")
    println("When result: ${when99}")
    println("Tailrec: ${tailrec799(5)}")
    val numbers = listOf(1, 2, 3, 4, 5)
    println("Sum: ${numbers.sum()}")
    println("Filtered: ${numbers.filter { it > 2 }}")
    
    val range = 1..5
    for (i in range) {
        println("Iteration: $i")
    }
    
    println("Program completed")
}
