
fun main() {
    val data = (1..20).toList()
    
    val result = data
        .asSequence()
        .filter { it % 2 == 0 }
        .map { it * 2 }
        .groupBy { it % 3 }
        .mapValues { (_, values) -> 
            values.sumOf { it.toLong() }
        }
        .filterValues { it > 50 }
        .toSortedMap()
    
    println("Result: $result")
    
    val matrix = List(5) { row ->
        List(5) { col ->
            row * col
        }
    }
    
    val flattened = matrix.flatten()
    val partitioned = flattened.partition { it % 2 == 0 }
    
    println("Matrix sum: ${flattened.sum()}")
    println("Evens: ${partitioned.first.size}")
    
    val zipped = data.zip(data.reversed())
        .map { (a, b) -> a to b }
        .associateBy({ it.first }, { it.second })
    
    println("Zipped: ${zipped.size} pairs")
}
