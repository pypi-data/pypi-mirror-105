package main

import (
"fmt")



#[async]
func nested() int {
return 42}


#[async]
func async_main() {
if !(await!(nested()) == 42) { panic("assert") }
fmt.Printf("%v\n","OK");}


func main() {
run(asyncio, async_main());}


