
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
    let mut a: &mut HashMap<i32, i32> = &mut [(1, 1), (2, 2), (3, 3)]
        .iter()
        .cloned()
        .collect::<HashMap<_, _>>();
    drop(a[2]);
    a[2] = 2;
    assert!(a.keys().collect::<Vec<_>>() == *vec![1, 3, 2]);
}
