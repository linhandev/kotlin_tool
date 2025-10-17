
typealias UserId = Int
typealias UserMap = Map<UserId, String>

data class User(val id: UserId, val name: String)

fun findUser(users: UserMap, id: UserId): String? {
    return users[id]
}

fun main() {
    val userMap: UserMap = mapOf(
        1 to "Alice",
        2 to "Bob",
        3 to "Charlie"
    )
    
    val user = User(1, "Alice")
    println("User: ${user.name}")
    println("Found: ${findUser(userMap, 2)}")
}
