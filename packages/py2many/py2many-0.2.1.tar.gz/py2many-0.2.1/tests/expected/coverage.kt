
fun do_pass() {
/* pass */
}

fun inline_pass() {
/* pass */
}

fun inline_ellipsis() {
/* ... */
}

fun indexing(): Int {
    var sum = 0
    var a: Array<Int> = arrayOf()
    for (i in (0..10 - 1)) {
        a += i
        sum += a[i]
    }
    return sum
}

fun infer_bool(code: Int): Boolean {
    return code in arrayOf(1, 2, 4)
}

fun show() {
    val a1 = 10
    val b1 = 15
    val b2 = 15
    assert(b1 == 15)
    assert(b2 == 15)
    val b9 = 2
    val b10 = 2
    assert(b9 == b10)
    var a2: Double = 2.1
    println("$a2")
    for (i in (0..10 - 1)) {
        println("$i")
    }
    for (i in (0..10 - 1 step 2)) {
        println("$i")
    }
    val a3 = -(a1)
    val a4 = (a3 + a1)
    println("$a4")
    val t1 = if (a1 > 5) 10 else 5
    assert(t1 == 10)
    val sum1 = indexing()
    println("$sum1")
    val a5 = arrayOf(1, 2, 3)
    if (true) {
        val __tmp1 = a5.size
        println("$__tmp1")
    }
    var a9: Array<String> = arrayOf("a", "b", "c", "d")
    if (true) {
        val __tmp2 = a9.size
        println("$__tmp2")
    }
    val a6 = setOf(1, 2, 3, 4)
    if (true) {
        val __tmp3 = a6.size
        println("$__tmp3")
    }
    val a7 = hashMapOf("a" to 1, "b" to 2)
    if (true) {
        val __tmp4 = a7.size
        println("$__tmp4")
    }
    val a8 = true
    if (a8) {
        println("true")
    } else {
        if (a4 > 0) {
            println("never get here")
        }
    }
    if (a1 == 11) {
        println("false")
    } else {
        println("true")
    }
    if (1 != null) {
        println("World is sane")
    }
    do_pass()
    inline_pass()
    val s = "1    2"
    println("$s")
}

fun main() {
    show()
}
