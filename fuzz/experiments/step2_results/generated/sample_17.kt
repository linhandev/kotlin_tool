
sealed class Resource<out T> {
    data class Success<T>(val data: T) : Resource<T>()
    data class Error(val message: String, val code: Int) : Resource<Nothing>()
    object Loading : Resource<Nothing>()
}

fun <T> handleResource(resource: Resource<T>): String {
    return when (resource) {
        is Resource.Success -> "Success: ${resource.data}"
        is Resource.Error -> "Error ${resource.code}: ${resource.message}"
        Resource.Loading -> "Loading..."
    }
}

fun main() {
    val success = Resource.Success(42)
    val error = Resource.Error("Not found", 404)
    val loading = Resource.Loading
    
    println(handleResource(success))
    println(handleResource(error))
    println(handleResource(loading))
}
