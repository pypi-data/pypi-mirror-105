#[async]
proc nested(): int =
  return 42

#[async]
proc async_main() =
  assert(await!(nested()) == 42)
  echo "OK"

proc main() =
  asyncio.run(async_main())

main()
