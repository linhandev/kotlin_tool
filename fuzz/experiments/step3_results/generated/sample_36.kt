
class Html {
    private val children = mutableListOf<Element>()
    
    fun head(init: Head.() -> Unit): Head {
        val head = Head()
        head.init()
        children.add(head)
        return head
    }
    
    fun body(init: Body.() -> Unit): Body {
        val body = Body()
        body.init()
        children.add(body)
        return body
    }
    
    override fun toString() = children.joinToString("
")
}

abstract class Element {
    protected val children = mutableListOf<Element>()
}

class Head : Element() {
    fun title(text: String) {
        children.add(object : Element() {
            override fun toString() = "<title>$text</title>"
        })
    }
    
    override fun toString() = "<head>${children.joinToString("")}</head>"
}

class Body : Element() {
    fun div(init: Div.() -> Unit): Div {
        val div = Div()
        div.init()
        children.add(div)
        return div
    }
    
    override fun toString() = "<body>${children.joinToString("")}</body>"
}

class Div : Element() {
    fun text(content: String) {
        children.add(object : Element() {
            override fun toString() = content
        })
    }
    
    override fun toString() = "<div>${children.joinToString("")}</div>"
}

fun html(init: Html.() -> Unit): Html {
    val html = Html()
    html.init()
    return html
}

fun main() {
    val page = html {
        head {
            title("My Page")
        }
        body {
            div {
                text("Hello")
            }
            div {
                text("World")
            }
        }
    }
    
    println(page.toString())
}
