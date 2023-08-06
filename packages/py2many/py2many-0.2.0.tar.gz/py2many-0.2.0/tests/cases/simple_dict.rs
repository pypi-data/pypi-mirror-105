
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
    let l_b: &HashMap<&str, i32> = &[("a", 0)].iter().cloned().collect::<HashMap<_, _>>();
    assert!(l_b.iter().any(|&x| x == "a"));
}
