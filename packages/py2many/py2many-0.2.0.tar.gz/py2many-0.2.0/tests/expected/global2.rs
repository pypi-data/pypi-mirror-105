
//! ```cargo
//! [package]
//! edition = "2018"
//! [dependencies]
//! lazy_static = "*"
//! ```

#![allow(clippy::upper_case_acronyms)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]
#![allow(unused_imports)]
#![allow(unused_mut)]
#![allow(unused_parens)]

extern crate lazy_static;
use lazy_static::lazy_static;
use std::collections::HashMap;
use std::collections::HashSet;

pub const code_0: i32 = 0;
pub const code_1: i32 = 1;
pub const code_a: &str = "a";
pub const code_b: &str = "b";
lazy_static! {
    pub static ref l_b: HashSet<&'static str> = [code_a].iter().cloned().collect::<HashSet<_>>();
}
lazy_static! {
    pub static ref l_c: HashMap<&'static str, i32> = [(code_b, code_0)]
        .iter()
        .cloned()
        .collect::<HashMap<_, _>>();
}
pub fn main() {
    assert!(l_b.iter().any(|&x| x == "a"));
    println!("{}", "OK");
}
