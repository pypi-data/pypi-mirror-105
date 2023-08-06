fun nested_containers(): Boolean {
    val CODES = hashMapOf("KEY" to arrayOf(1, 3))
    return 1 in CODES["KEY"]
}

fun main() {
    if (nested_containers()) {
        println("OK")
    }
}
