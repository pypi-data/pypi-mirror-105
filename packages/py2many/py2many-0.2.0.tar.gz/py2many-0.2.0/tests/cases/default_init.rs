
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

pub struct Rectangle {
    pub height: ST0,
    pub length: ST1,
}

impl Rectangle {
    pub fn __init__<T0, T1>(&self, height: T0, length: T1) {
        self.height = height;
        self.length = length;
    }
}
pub fn main() {
    let r: Rectangle = Rectangle {};
}
