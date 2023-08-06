package main

import (
"fmt"
iter "github.com/hgfischer/go-iter")




func TestPython(iterations int) {
var iteration int = 0
var total float64 = float(0.0)
var array_length int = 1000
var array []int = iter.NewIntSeq(iter.Start(0), iter.Stop(array_length)).All().iter().map(|i| i).collect::<Vec<_>>()
fmt.Printf("%v %v\n","iterations", iterations);
for iteration < iterations {
var innerloop int = 0
for innerloop < 100 {
total += array[((iteration + innerloop) % array_length)];
innerloop += 1;
}
iteration += 1;
}
if(total == 15150) {
fmt.Printf("%v\n","OK");
}
array.drop()}


func main() {
TestPython(3);}


