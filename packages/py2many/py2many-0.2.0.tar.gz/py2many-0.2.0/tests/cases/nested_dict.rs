
//! ```cargo
//! [package]
//! edition = "2018"
//! [dependencies]
//!
//! ```

#![allow(clippy::upper_case_acronyms)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]
#![allow(unused_imports)]
#![allow(unused_mut)]
#![allow(unused_parens)]

use std::collections;
use std::collections::HashMap;

pub fn nested_containers() -> bool {
    let CODES: &HashMap<&str, Vec<i32>> = &[("KEY", vec![1, 3])]
        .iter()
        .cloned()
        .collect::<HashMap<_, _>>();
    return CODES["KEY"].iter().any(|&x| x == 1);
}

pub fn main() {
    if nested_containers() {
        println!("{}", "OK");
    }
}
