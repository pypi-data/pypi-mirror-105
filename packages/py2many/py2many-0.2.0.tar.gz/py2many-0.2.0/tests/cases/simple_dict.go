package main

import (
"github.com/google/go-cmp/cmp"
"fmt"
"github.com/adsharma/py2many/pygo/runtime")



var LB = map[string]int{"a": 0}
if !(pygo.Contains(LB, "a")) { panic("assert") }
