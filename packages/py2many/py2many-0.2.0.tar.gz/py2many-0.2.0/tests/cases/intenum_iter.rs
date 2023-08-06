
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
use std::collections::HashMap;

#[derive(Clone, Eq, Hash, PartialEq)]
pub enum Colors {
    RED,
    GREEN,
    BLUE,
}

pub fn main() {
    for val in Colors {
        println!("{}", val);
    }
}
