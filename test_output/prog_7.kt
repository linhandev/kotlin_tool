// Auto-generated diverse Kotlin program
// Testing Kotlin Native compiler backend
import kotlin.random.Random

// Feature: generics
class Gen699<T>(val value: T) {
    fun get(): T = value
    fun <R> map(fn: (T) -> R): Gen699<R> = Gen699(fn(value))
}

// Feature: destructuring
fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

// Feature: sequences
val seq = generateSequence(1) { if (it < 100) it * 2 else null }
val seqList = seq.take(5).toList()

// Feature: ranges
val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

// Feature: infix_function
infix fun Int.infix813(other: Int): Int = this + other

// Feature: sealed_class
sealed class Sealed286 {
    data class Sub0(val value: Int) : Sealed286()
    object Sub1 : Sealed286()
}

// Feature: operator_overload
data class Op661(val value: Int) {
    operator fun plus(other: Op661): Op661 = Op661(value + other.value)
    operator fun times(factor: Int): Op661 = Op661(value * factor)
}

// Feature: data_class
data class Data141(val prop0: Double, val prop1: Double, val prop2: Int)

// Feature: companion_object
class Comp865 {
    companion object {
        const val CONST_VAL = 42
        fun create(): Comp865 = Comp865()
    }
}

// Feature: lambda
val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

// Feature: extension_function
fun Int.ext312(): Int = this * 2

// Feature: inline_function
inline fun inline54(block: () -> Unit) { block() }

// Feature: nullable_types
val nullable1: String? = if (Random.nextBoolean()) "value" else null
val length1 = nullable1?.length ?: 0
val safe1 = nullable1?.uppercase() ?: "DEFAULT"

// Feature: vararg
fun vararg156(vararg items: Int): Int = items.sum()

// Feature: enum_class
enum class Enum798 { VALUE0, VALUE1, VALUE2 }

// Feature: property_delegation
class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

// Feature: tailrec
tailrec fun tailrec836(n: Int, acc: Int = 1): Int {
    if (n <= 1) return acc
    return tailrec836(n - 1, acc * n)
}

// Feature: default_parameters
fun default909(x: Int = 10, y: String = "default"): String = "x=$x, y=$y"

fun main() {
    println("Program started - testing diverse Kotlin features")
    val numbers = listOf(1, 2, 3, 4, 5)
    println("Sum: ${numbers.sum()}")
    println("Filtered: ${numbers.filter { it > 2 }}")
    
    val range = 1..5
    for (i in range) {
        println("Iteration: $i")
    }
    
    println("Program completed")
}
