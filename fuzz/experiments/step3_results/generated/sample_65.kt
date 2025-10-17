
interface Serializable {
    fun serialize(): String
}

data class Entity(val id: Int, val name: String, val active: Boolean) : Serializable {
    override fun serialize(): String = "Entity($id, $name, $active)"
}

inline fun <reified T> createInstance(vararg args: Any): String {
    return "${T::class.simpleName}(${args.joinToString(", ")})"
}

inline fun <reified T> typeCheck(value: Any): Boolean {
    return value is T
}

fun main() {
    val entity = Entity(1, "Test", true)
    println("Serialized: ${entity.serialize()}")
    
    val created = createInstance<Entity>(2, "New", false)
    println("Created: $created")
    
    println("Is Entity: ${typeCheck<Entity>(entity)}")
    println("Is String: ${typeCheck<String>(entity)}")
    
    val types = listOf("String", 42, true, 3.14)
    types.forEach { value ->
        when (value) {
            is String -> println("String: $value")
            is Int -> println("Int: $value")
            is Boolean -> println("Boolean: $value")
            is Double -> println("Double: $value")
        }
    }
}
