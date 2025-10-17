fun findUser(id: Int): String? {
    return if (id > 0) "User $id" else null
}

fun main() {
    val user1 = findUser(1)
    val user2 = findUser(-1)
    
    println("User 1: ${user1 ?: "Not found"}")
    println("User 2: ${user2 ?: "Not found"}")
}
