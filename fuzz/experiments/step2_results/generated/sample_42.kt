
interface Producer<out T> {
    fun produce(): T
}

interface Consumer<in T> {
    fun consume(item: T)
}

class StringProducer : Producer<String> {
    override fun produce(): String = "Hello"
}

class AnyConsumer : Consumer<Any> {
    override fun consume(item: Any) {
        println("Consumed: $item")
    }
}

fun main() {
    val producer: Producer<String> = StringProducer()
    val consumer: Consumer<String> = AnyConsumer()
    
    consumer.consume(producer.produce())
}
