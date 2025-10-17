sealed class Result {
    data class Success(val data: String) : Result()
    data class Error(val message: String) : Result()
    object Loading : Result()
}

fun process(result: Result): String = when (result) {
    is Result.Success -> "Success: ${result.data}"
    is Result.Error -> "Error: ${result.message}"
    Result.Loading -> "Loading..."
}

fun main() {
    println(process(Result.Success("Done")))
    println(process(Result.Error("Failed")))
    println(process(Result.Loading))
}
