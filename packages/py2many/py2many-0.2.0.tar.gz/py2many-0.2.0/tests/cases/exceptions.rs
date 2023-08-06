
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

pub fn show() {
    let try_dummy = {
        //unsupported
        raise!(Exception("foo")); //unsupported
    };
    let except!(Exception) = {
        //unsupported
        println!("{}", "caught");
    };
    let try_dummy = {
        //unsupported
        (3 / 0);
    };
    let except!(ZeroDivisionError) = {
        //unsupported
        println!("{}", "OK");
    };
    let try_dummy = {
        //unsupported
        raise!(Exception("foo")); //unsupported
    };
    let except!() = {
        //unsupported
        println!("{}", "Got it");
    };
}

pub fn main() {
    show();
}
