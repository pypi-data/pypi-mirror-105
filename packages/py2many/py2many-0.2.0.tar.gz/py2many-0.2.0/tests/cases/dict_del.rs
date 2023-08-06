
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

pub fn main() {
    let a: &HashMap<i32, i32> = &[(1, 1)].iter().cloned().collect::<HashMap<_, _>>();
    drop(a[1]);
    assert!(!(a));
}
