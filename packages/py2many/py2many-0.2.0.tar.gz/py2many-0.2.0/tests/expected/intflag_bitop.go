package main

import (
	"fmt"
	"github.com/google/go-cmp/cmp"
)

type Permissions int

const (
	R Permissions = 1
	W             = 2
	X             = 16
)

var a Permissions = (R | W)

func Main() {
	if a & R {
		fmt.Printf("%v\n", "R")
	}
}
