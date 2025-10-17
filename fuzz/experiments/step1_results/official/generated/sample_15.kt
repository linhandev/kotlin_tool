enum class Color(val rgb: Int) {
    RED(0xFF0000),
    GREEN(0x00FF00),
    BLUE(0x0000FF)
}

fun main() {
    for (color in Color.values()) {
        println("${color.name}: 0x${color.rgb.toString(16)}")
    }
}
