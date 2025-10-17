// Auto-generated diverse Kotlin program
// Testing Kotlin Native compiler backend
import kotlin.random.Random

// Feature: destructuring
fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

// Feature: property_delegation
class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

// Feature: extension_function
fun List<Int>.ext584(): Int = this.sum()

// Feature: enum_class
enum class Enum647 { VALUE0, VALUE1 }

// Feature: inline_function
inline fun inline686(block: () -> Unit) { block() }

// Feature: default_parameters
fun default12(x: Int = 10, y: String = "default"): String = "x=$x, y=$y"

// Feature: type_alias
typealias TypeAlias791 = Map<String, List<Int>>

// Feature: nested_class
class Outer195 {
    class Nested {
        fun doSomething() = 123
    }
}

// Feature: when_expression
val when237 = when (Random.nextInt(0, 5)) {
    0 -> "zero"
    1, 2 -> "one or two"
    in 3..4 -> "three or four"
    else -> "other"
}

// Feature: vararg
fun vararg967(vararg items: Int): Int = items.sum()

// Feature: ranges
val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

// Feature: sequences
val seq = generateSequence(1) { if (it < 100) it * 2 else null }
val seqList = seq.take(5).toList()

// Feature: generics
class Gen255<T>(val value: T) {
    fun get(): T = value
    fun <R> map(fn: (T) -> R): Gen255<R> = Gen255(fn(value))
}

// Feature: tailrec
tailrec fun tailrec101(n: Int, acc: Int = 1): Int {
    if (n <= 1) return acc
    return tailrec101(n - 1, acc * n)
}

// Feature: infix_function
infix fun Int.infix9(other: Int): Int = this + other

// Feature: data_class
data class Data790(val prop0: Int, val prop1: Boolean, val prop2: Double, val prop3: Int)

// Feature: sealed_class
sealed class Sealed960 {
    object Sub0 : Sealed960()
    data class Sub1(val value: Int) : Sealed960()
    object Sub2 : Sealed960()
}

// Feature: companion_object
class Comp161 {
    companion object {
        const val CONST_VAL = 42
        fun create(): Comp161 = Comp161()
    }
}

fun main() {
    println("Program started - testing diverse Kotlin features")
    println("Enum: ${Enum647.values()[0]}")
    val numbers = listOf(1, 2, 3, 4, 5)
    println("Sum: ${numbers.sum()}")
    println("Filtered: ${numbers.filter { it > 2 }}")
    
    val range = 1..5
    for (i in range) {
        println("Iteration: $i")
    }
    
    println("Program completed")
}
