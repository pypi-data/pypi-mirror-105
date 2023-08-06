suspend fun nested(): Int {
    return 42
}

suspend fun async_main() {
    assert(nested().await() == 42)
    println("OK")
}

fun main() {
    asyncio.run(async_main())
}
