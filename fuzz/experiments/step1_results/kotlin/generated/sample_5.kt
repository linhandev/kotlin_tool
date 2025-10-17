data class User(val id: Int, val name: String, val email: String)

fun main() {
    val user1 = User(1, "Bob", "bob@example.com")
    val user2 = user1.copy(name = "Alice")
    
    println("User 1: $user1")
    println("User 2: $user2")
}
