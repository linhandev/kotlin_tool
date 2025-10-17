// Auto-generated diverse Kotlin program
// Testing Kotlin Native compiler backend
import kotlin.random.Random

// Feature: extension_function
fun String.ext662(): String = this.uppercase()

// Feature: lambda
val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

// Feature: inline_function
inline fun inline918(block: () -> Unit) { block() }

// Feature: type_alias
typealias TypeAlias406 = Map<String, List<Int>>

// Feature: infix_function
infix fun Int.infix479(other: Int): Int = this + other

// Feature: generics
class Gen762<T>(val value: T) {
    fun get(): T = value
    fun <R> map(fn: (T) -> R): Gen762<R> = Gen762(fn(value))
}

// Feature: ranges
val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

// Feature: property_delegation
class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

// Feature: default_parameters
fun default821(x: Int = 10, y: String = "default"): String = "x=$x, y=$y"

// Feature: sealed_class
sealed class Sealed289 {
    object Sub0 : Sealed289()
    data class Sub1(val value: Int) : Sealed289()
    data class Sub2(val value: Int) : Sealed289()
}

// Feature: nullable_types
val nullable1: String? = if (Random.nextBoolean()) "value" else null
val length1 = nullable1?.length ?: 0
val safe1 = nullable1?.uppercase() ?: "DEFAULT"

// Feature: data_class
data class Data293(val prop0: Boolean, val prop1: Double)

// Feature: companion_object
class Comp953 {
    companion object {
        const val CONST_VAL = 42
        fun create(): Comp953 = Comp953()
    }
}

// Feature: enum_class
enum class Enum675 { VALUE0, VALUE1 }

// Feature: vararg
fun vararg758(vararg items: Int): Int = items.sum()

// Feature: when_expression
val when503 = when (Random.nextInt(0, 5)) {
    0 -> "zero"
    1, 2 -> "one or two"
    in 3..4 -> "three or four"
    else -> "other"
}

// Feature: tailrec
tailrec fun tailrec221(n: Int, acc: Int = 1): Int {
    if (n <= 1) return acc
    return tailrec221(n - 1, acc * n)
}

// Feature: sequences
val seq = generateSequence(1) { if (it < 100) it * 2 else null }
val seqList = seq.take(5).toList()

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
