
sealed class Expression {
    data class Const(val value: Int) : Expression()
    data class Add(val left: Expression, val right: Expression) : Expression()
    data class Multiply(val left: Expression, val right: Expression) : Expression()
}

fun eval(expr: Expression): Int = when (expr) {
    is Expression.Const -> expr.value
    is Expression.Add -> eval(expr.left) + eval(expr.right)
    is Expression.Multiply -> eval(expr.left) * eval(expr.right)
}

fun main() {
    val expr = Expression.Add(
        Expression.Const(1),
        Expression.Multiply(Expression.Const(2), Expression.Const(3))
    )
    println("Result: ${eval(expr)}")
}
