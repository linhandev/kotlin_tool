// Auto-generated diverse Kotlin program
// Testing Kotlin Native compiler backend
import kotlin.random.Random

// Feature: lambda
val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

// Feature: infix_function
infix fun Int.infix38(other: Int): Int = this + other

// Feature: type_alias
typealias TypeAlias956 = Map<String, List<Int>>

// Feature: companion_object
class Comp879 {
    companion object {
        const val CONST_VAL = 42
        fun create(): Comp879 = Comp879()
    }
}

// Feature: operator_overload
data class Op391(val value: Int) {
    operator fun plus(other: Op391): Op391 = Op391(value + other.value)
    operator fun times(factor: Int): Op391 = Op391(value * factor)
}

// Feature: destructuring
fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

// Feature: sealed_class
sealed class Sealed937 {
    data class Sub0(val value: Int) : Sealed937()
    data class Sub1(val value: Int) : Sealed937()
    object Sub2 : Sealed937()
}

// Feature: data_class
data class Data135(val prop0: Int, val prop1: Double, val prop2: Boolean, val prop3: Double)

// Feature: ranges
val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

// Feature: nullable_types
val nullable1: String? = if (Random.nextBoolean()) "value" else null
val length1 = nullable1?.length ?: 0
val safe1 = nullable1?.uppercase() ?: "DEFAULT"

// Feature: extension_function
fun Int.ext650(): Int = this * 2

// Feature: default_parameters
fun default733(x: Int = 10, y: String = "default"): String = "x=$x, y=$y"

// Feature: when_expression
val when660 = when (Random.nextInt(0, 5)) {
    0 -> "zero"
    1, 2 -> "one or two"
    in 3..4 -> "three or four"
    else -> "other"
}

// Feature: inline_function
inline fun inline715(block: () -> Unit) { block() }

// Feature: vararg
fun vararg202(vararg items: Int): Int = items.sum()

// Feature: tailrec
tailrec fun tailrec910(n: Int, acc: Int = 1): Int {
    if (n <= 1) return acc
    return tailrec910(n - 1, acc * n)
}

// Feature: property_delegation
class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

// Feature: generics
class Gen61<T>(val value: T) {
    fun get(): T = value
    fun <R> map(fn: (T) -> R): Gen61<R> = Gen61(fn(value))
}

fun main() {
    println("Program started - testing diverse Kotlin features")
    println("Lambda: ${lambda1(21)}")
    println("Higher-order: ${higherOrder { it + 1 }}")
    val numbers = listOf(1, 2, 3, 4, 5)
    println("Sum: ${numbers.sum()}")
    println("Filtered: ${numbers.filter { it > 2 }}")
    
    val range = 1..5
    for (i in range) {
        println("Iteration: $i")
    }
    
    println("Program completed")
}
