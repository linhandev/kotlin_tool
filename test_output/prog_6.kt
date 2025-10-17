// Auto-generated diverse Kotlin program
// Testing Kotlin Native compiler backend
import kotlin.random.Random

// Feature: companion_object
class Comp986 {
    companion object {
        const val CONST_VAL = 42
        fun create(): Comp986 = Comp986()
    }
}

// Feature: vararg
fun vararg632(vararg items: Int): Int = items.sum()

// Feature: sequences
val seq = generateSequence(1) { if (it < 100) it * 2 else null }
val seqList = seq.take(5).toList()

// Feature: type_alias
typealias TypeAlias624 = Map<String, List<Int>>

// Feature: destructuring
fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

// Feature: extension_function
fun Int.ext915(): Int = this * 2

// Feature: infix_function
infix fun Int.infix804(other: Int): Int = this + other

// Feature: default_parameters
fun default524(x: Int = 10, y: String = "default"): String = "x=$x, y=$y"

// Feature: nested_class
class Outer272 {
    class Nested {
        fun doSomething() = 123
    }
}

// Feature: nullable_types
val nullable1: String? = if (Random.nextBoolean()) "value" else null
val length1 = nullable1?.length ?: 0
val safe1 = nullable1?.uppercase() ?: "DEFAULT"

// Feature: generics
class Gen615<T>(val value: T) {
    fun get(): T = value
    fun <R> map(fn: (T) -> R): Gen615<R> = Gen615(fn(value))
}

// Feature: sealed_class
sealed class Sealed559 {
    data class Sub0(val value: Int) : Sealed559()
    data class Sub1(val value: Int) : Sealed559()
    data class Sub2(val value: Int) : Sealed559()
}

// Feature: data_class
data class Data624(val prop0: Boolean, val prop1: Double)

// Feature: operator_overload
data class Op917(val value: Int) {
    operator fun plus(other: Op917): Op917 = Op917(value + other.value)
    operator fun times(factor: Int): Op917 = Op917(value * factor)
}

// Feature: lambda
val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

// Feature: when_expression
val when873 = when (Random.nextInt(0, 5)) {
    0 -> "zero"
    1, 2 -> "one or two"
    in 3..4 -> "three or four"
    else -> "other"
}

// Feature: enum_class
enum class Enum652 { VALUE0, VALUE1 }

// Feature: ranges
val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

fun main() {
    println("Program started - testing diverse Kotlin features")
    println("Vararg: ${vararg632(1, 2, 3)}")
    val numbers = listOf(1, 2, 3, 4, 5)
    println("Sum: ${numbers.sum()}")
    println("Filtered: ${numbers.filter { it > 2 }}")
    
    val range = 1..5
    for (i in range) {
        println("Iteration: $i")
    }
    
    println("Program completed")
}
