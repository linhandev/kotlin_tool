
data class Matrix(val rows: Int, val cols: Int, val data: List<List<Int>>) {
    operator fun plus(other: Matrix): Matrix {
        require(rows == other.rows && cols == other.cols)
        val result = data.zip(other.data).map { (r1, r2) ->
            r1.zip(r2).map { (a, b) -> a + b }
        }
        return Matrix(rows, cols, result)
    }
    
    operator fun times(scalar: Int): Matrix {
        val result = data.map { row -> row.map { it * scalar } }
        return Matrix(rows, cols, result)
    }
    
    operator fun get(i: Int, j: Int): Int = data[i][j]
    
    operator fun invoke(i: Int, j: Int): Int = data[i][j]
}

data class Complex(val real: Double, val imag: Double) {
    operator fun plus(other: Complex) = Complex(real + other.real, imag + other.imag)
    operator fun minus(other: Complex) = Complex(real - other.real, imag - other.imag)
    operator fun times(other: Complex) = Complex(
        real * other.real - imag * other.imag,
        real * other.imag + imag * other.real
    )
    
    override fun toString() = "$real + ${imag}i"
}

fun main() {
    val m1 = Matrix(2, 2, listOf(listOf(1, 2), listOf(3, 4)))
    val m2 = Matrix(2, 2, listOf(listOf(5, 6), listOf(7, 8)))
    
    val m3 = m1 + m2
    val m4 = m1 * 2
    
    println("m1[0,0] = ${m1[0, 0]}")
    println("m1(1,1) = ${m1(1, 1)}")
    
    val c1 = Complex(1.0, 2.0)
    val c2 = Complex(3.0, 4.0)
    
    println("c1 + c2 = ${c1 + c2}")
    println("c1 * c2 = ${c1 * c2}")
}
