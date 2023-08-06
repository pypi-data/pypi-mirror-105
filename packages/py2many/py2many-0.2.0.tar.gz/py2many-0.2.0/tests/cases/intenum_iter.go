package main

import (
	"fmt"
	"github.com/google/go-cmp/cmp"
)

type Colors int

const (
	RED   Colors = iota
	GREEN        = iota
	BLUE         = iota
)

func Main() {
	for _, val := range Colors {
		fmt.Printf("%v\n", val)
	}
}
