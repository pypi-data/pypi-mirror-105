package main

import (
"github.com/google/go-cmp/cmp"
"fmt"
"github.com/adsharma/py2many/pygo/runtime")



var foo, baz, qux = 4, 5, 6
if !(foo != baz != qux) { panic("assert") }
