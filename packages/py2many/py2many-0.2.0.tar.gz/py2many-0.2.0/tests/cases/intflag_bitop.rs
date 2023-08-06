
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

flags! {
    pub enum Permissions: c_int {
        R = 1,
        W = 2,
        X = 16,
    }
}

pub const a: Permissions = (Permissions::R | Permissions::W);
pub fn main() {
    if (a & Permissions::R) {
        println!("{}", "R");
    }
}
