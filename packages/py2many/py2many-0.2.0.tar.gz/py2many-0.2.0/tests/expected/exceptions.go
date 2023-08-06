package main

import (
"fmt")



func Show() {
let try_dummy = { //unsupported
raise!(Exception("foo")); //unsupported
};
let except!(Exception) = { //unsupported
fmt.Printf("%v\n","caught");
};
let try_dummy = { //unsupported
(3/0);
};
let except!(ZeroDivisionError) = { //unsupported
fmt.Printf("%v\n","OK");
};
let try_dummy = { //unsupported
raise!(Exception("foo")); //unsupported
};
let except!() = { //unsupported
fmt.Printf("%v\n","Got it");
};}


func main() {
Show();}


