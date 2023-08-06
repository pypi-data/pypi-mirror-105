
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

pub fn foo() {
    let a: i32 = 10;
    let b: i32 = a;
    assert!(b == 10);
    println!("{}", b);
}

pub fn main() {
    foo();
}
