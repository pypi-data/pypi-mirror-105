
//! ```cargo
//! [package]
//! edition = "2018"
//! [dependencies]
//!
//! ```

#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]
#![allow(unused_imports)]
#![allow(unused_mut)]
#![allow(unused_parens)]

use std::collections;

pub fn main() {
    let b1: i32 = 15;
    let b2: _ = 15;
    assert!(b1 == b2 as i32);
}
