// Auto-generated diverse Kotlin program
// Testing Kotlin Native compiler backend
import kotlin.random.Random

// Feature: inline_function
inline fun inline625(block: () -> Unit) { block() }

// Feature: when_expression
val when385 = when (Random.nextInt(0, 5)) {
    0 -> "zero"
    1, 2 -> "one or two"
    in 3..4 -> "three or four"
    else -> "other"
}

// Feature: sealed_class
sealed class Sealed482 {
    data class Sub0(val value: Int) : Sealed482()
    object Sub1 : Sealed482()
}

// Feature: extension_function
fun String.ext460(): String = this.uppercase()

// Feature: property_delegation
class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

// Feature: ranges
val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

// Feature: type_alias
typealias TypeAlias339 = Map<String, List<Int>>

// Feature: vararg
fun vararg8(vararg items: Int): Int = items.sum()

// Feature: sequences
val seq = generateSequence(1) { if (it < 100) it * 2 else null }
val seqList = seq.take(5).toList()

// Feature: companion_object
class Comp58 {
    companion object {
        const val CONST_VAL = 42
        fun create(): Comp58 = Comp58()
    }
}

// Feature: destructuring
fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

// Feature: operator_overload
data class Op206(val value: Int) {
    operator fun plus(other: Op206): Op206 = Op206(value + other.value)
    operator fun times(factor: Int): Op206 = Op206(value * factor)
}

// Feature: data_class
data class Data369(val prop0: Double, val prop1: Boolean)

// Feature: enum_class
enum class Enum828 { VALUE0, VALUE1, VALUE2, VALUE3 }

// Feature: nullable_types
val nullable1: String? = if (Random.nextBoolean()) "value" else null
val length1 = nullable1?.length ?: 0
val safe1 = nullable1?.uppercase() ?: "DEFAULT"

// Feature: tailrec
tailrec fun tailrec176(n: Int, acc: Int = 1): Int {
    if (n <= 1) return acc
    return tailrec176(n - 1, acc * n)
}

// Feature: lambda
val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

// Feature: infix_function
infix fun Int.infix181(other: Int): Int = this + other

fun main() {
    println("Program started - testing diverse Kotlin features")
    println("When result: ${when385}")
    val numbers = listOf(1, 2, 3, 4, 5)
    println("Sum: ${numbers.sum()}")
    println("Filtered: ${numbers.filter { it > 2 }}")
    
    val range = 1..5
    for (i in range) {
        println("Iteration: $i")
    }
    
    println("Program completed")
}
