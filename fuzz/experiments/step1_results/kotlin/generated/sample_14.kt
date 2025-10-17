interface Clickable {
    fun click()
}

fun main() {
    val button = object : Clickable {
        override fun click() {
            println("Button clicked!")
        }
    }
    
    button.click()
}
