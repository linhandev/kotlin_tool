
class HtmlBuilder {
    private val elements = mutableListOf<String>()
    
    fun tag(name: String, content: String) {
        elements.add("<$name>$content</$name>")
    }
    
    fun build(): String = elements.joinToString("
")
}

fun html(init: HtmlBuilder.() -> Unit): String {
    val builder = HtmlBuilder()
    builder.init()
    return builder.build()
}

fun main() {
    val result = html {
        tag("h1", "Title")
        tag("p", "Paragraph")
    }
    println(result)
}
