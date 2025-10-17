// Auto-generated diverse Kotlin program
// Testing Kotlin Native compiler backend
import kotlin.random.Random

// Feature: nested_class
class Outer551 {
    class Nested {
        fun doSomething() = 123
    }
}

// Feature: type_alias
typealias TypeAlias3 = Map<String, List<Int>>

// Feature: destructuring
fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

// Feature: operator_overload
data class Op848(val value: Int) {
    operator fun plus(other: Op848): Op848 = Op848(value + other.value)
    operator fun times(factor: Int): Op848 = Op848(value * factor)
}

// Feature: ranges
val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

// Feature: inline_function
inline fun inline431(block: () -> Unit) { block() }

// Feature: extension_function
fun String.ext404(): String = this.uppercase()

// Feature: property_delegation
class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

// Feature: lambda
val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

// Feature: sealed_class
sealed class Sealed955 {
    data class Sub0(val value: Int) : Sealed955()
    data class Sub1(val value: Int) : Sealed955()
}

// Feature: when_expression
val when893 = when (Random.nextInt(0, 5)) {
    0 -> "zero"
    1, 2 -> "one or two"
    in 3..4 -> "three or four"
    else -> "other"
}

// Feature: enum_class
enum class Enum320 { VALUE0, VALUE1, VALUE2 }

// Feature: infix_function
infix fun Int.infix399(other: Int): Int = this + other

// Feature: default_parameters
fun default587(x: Int = 10, y: String = "default"): String = "x=$x, y=$y"

// Feature: data_class
data class Data760(val prop0: Double, val prop1: Double, val prop2: Double, val prop3: Double)

// Feature: companion_object
class Comp937 {
    companion object {
        const val CONST_VAL = 42
        fun create(): Comp937 = Comp937()
    }
}

// Feature: nullable_types
val nullable1: String? = if (Random.nextBoolean()) "value" else null
val length1 = nullable1?.length ?: 0
val safe1 = nullable1?.uppercase() ?: "DEFAULT"

// Feature: vararg
fun vararg944(vararg items: Int): Int = items.sum()

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
