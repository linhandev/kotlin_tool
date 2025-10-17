// Auto-generated diverse Kotlin program
// Testing Kotlin Native compiler backend
import kotlin.random.Random

// Feature: lambda
val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

// Feature: ranges
val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

// Feature: extension_function
fun String.ext960(): String = this.uppercase()

// Feature: sealed_class
sealed class Sealed737 {
    data class Sub0(val value: Int) : Sealed737()
    object Sub1 : Sealed737()
}

// Feature: type_alias
typealias TypeAlias330 = Map<String, List<Int>>

// Feature: destructuring
fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

// Feature: enum_class
enum class Enum230 { VALUE0, VALUE1 }

// Feature: data_class
data class Data45(val prop0: String, val prop1: Boolean)

// Feature: operator_overload
data class Op962(val value: Int) {
    operator fun plus(other: Op962): Op962 = Op962(value + other.value)
    operator fun times(factor: Int): Op962 = Op962(value * factor)
}

// Feature: nested_class
class Outer379 {
    class Nested {
        fun doSomething() = 123
    }
}

// Feature: when_expression
val when70 = when (Random.nextInt(0, 5)) {
    0 -> "zero"
    1, 2 -> "one or two"
    in 3..4 -> "three or four"
    else -> "other"
}

// Feature: property_delegation
class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

// Feature: default_parameters
fun default419(x: Int = 10, y: String = "default"): String = "x=$x, y=$y"

// Feature: companion_object
class Comp310 {
    companion object {
        const val CONST_VAL = 42
        fun create(): Comp310 = Comp310()
    }
}

// Feature: vararg
fun vararg501(vararg items: Int): Int = items.sum()

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
