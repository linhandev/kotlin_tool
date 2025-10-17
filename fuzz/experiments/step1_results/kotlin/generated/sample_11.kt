fun operation(x: Int, y: Int, op: (Int, Int) -> Int): Int {
    return op(x, y)
}

fun main() {
    val sum = operation(5, 3) { a, b -> a + b }
    val product = operation(5, 3) { a, b -> a * b }
    
    println("Sum: $sum")
    println("Product: $product")
}
