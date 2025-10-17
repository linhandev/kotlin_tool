
inline fun <reified T> create(): String {
    return T::class.simpleName ?: "Unknown"
}

inline fun <reified T> checkType(value: Any): Boolean {
    return value is T
}

fun main() {
    println("Created: ${create<String>()}")
    println("Created: ${create<Int>()}")
    
    println("Is String: ${checkType<String>("hello")}")
    println("Is Int: ${checkType<Int>("hello")}")
}
