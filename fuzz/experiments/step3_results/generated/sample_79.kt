
sealed class Either<out L, out R> {
    data class Left<L>(val value: L) : Either<L, Nothing>()
    data class Right<R>(val value: R) : Either<Nothing, R>()
    
    fun <T> fold(left: (L) -> T, right: (R) -> T): T = when (this) {
        is Left -> left(value)
        is Right -> right(value)
    }
    
    fun <T> map(f: (R) -> T): Either<L, T> = when (this) {
        is Left -> this
        is Right -> Right(f(value))
    }
}

data class State<S, out A>(val run: (S) -> Pair<S, A>) {
    fun <B> map(f: (A) -> B): State<S, B> = State { s ->
        val (s2, a) = run(s)
        s2 to f(a)
    }
    
    fun <B> flatMap(f: (A) -> State<S, B>): State<S, B> = State { s ->
        val (s2, a) = run(s)
        f(a).run(s2)
    }
}

fun main() {
    val left: Either<String, Int> = Either.Left("error")
    val right: Either<String, Int> = Either.Right(42)
    
    println(left.fold({ "Left: $it" }, { "Right: $it" }))
    println(right.fold({ "Left: $it" }, { "Right: $it" }))
    
    val mapped = right.map { it * 2 }
    println(mapped.fold({ "Error: $it" }, { "Result: $it" }))
    
    val state1 = State<Int, String> { s -> (s + 1) to "Value: $s" }
    val state2 = state1.map { it.uppercase() }
    
    val (finalState, result) = state2.run(10)
    println("State: $finalState, Result: $result")
}
