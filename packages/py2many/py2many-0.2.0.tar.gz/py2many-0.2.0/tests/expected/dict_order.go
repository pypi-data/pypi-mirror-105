package main

import (
"fmt"
"github.com/google/go-cmp/cmp")



var a = map[int]int{1: 1, 2: 2, 3: 3}
a[2].drop()
a[2] = 2
if !(cmp.Equal(list(a.keys()), []int{1, 3, 2})) { panic("assert") }
