
//! ```cargo
//! [package]
//! edition = "2018"
//! [dependencies]
//! flagset = "*"
//! ```

#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]
#![allow(unused_imports)]
#![allow(unused_mut)]
#![allow(unused_parens)]

extern crate flagset;
use flagset::flags;
use std::collections;
use std::collections::HashMap;
use std::os::raw::c_int;

pub fn main() {
    let ab: _ = "{}{}".format("a", "b");
}
