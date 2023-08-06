class A {
    val B: ST0

    val B = "FOO"
}

fun main() {
    assert(A.B == "FOO")
}
