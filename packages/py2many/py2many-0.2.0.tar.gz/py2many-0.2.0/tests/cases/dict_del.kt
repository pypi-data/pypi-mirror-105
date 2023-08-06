fun main() {
    val a = hashMapOf(1 to 1)
    a[1].drop()
    assert(!(a))
}
