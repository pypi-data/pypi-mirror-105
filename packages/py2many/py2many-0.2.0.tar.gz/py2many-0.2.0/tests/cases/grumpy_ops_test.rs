#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]
#![allow(unused_imports)]
#![allow(unused_mut)]
#![allow(unused_parens)]

use std::collections;

pub fn test_bool_ops() {
    assert!("foo" || "bar" == "foo");
    assert!("" || 123 as i32 == 123);
    assert!(0 && 3.14 as i32 == 0);
    assert!(true && false as bool == false);
    assert!(0 || "a" && "b" == "b");
    assert!(1 && "a" || "b" == "a");
}

pub fn test_bool_ops_lazy_eval() -> bool {
    pub fn Yes() -> bool {
        ran.push("Yes");
        return true;
    }

    pub fn No() -> bool {
        ran.push("No");
        return false;
    }

    let mut ran: List = vec![];
    assert!(Yes() || No());
    assert!(ran == *vec!["Yes"]);
    ran = vec![];
    assert!(!(Yes() && Yes() && No()));
    assert!(ran == *vec!["Yes", "Yes", "No"]);
    ran = vec![];
    assert!(!(Yes() && No() && Yes()));
    assert!(ran == *vec!["Yes", "No"]);
    ran = vec![];
    assert!(No() || No() || Yes());
    assert!(ran == *vec!["No", "No", "Yes"]);
    ran = vec![];
    assert!(Yes() || Yes() || Yes());
    assert!(ran == *vec!["Yes"]);
}

pub fn test_neg() {
    let mut x: i32 = 12;
    assert!(-(x) == -12);
    x = 1.1;
    assert!(-(x) as f64 == -1.1);
    x = 0.0;
    assert!(-(x) as f64 == -0.0);
    x = f64::from("inf");
    assert!(math.isinf(-(x)));
    x = -f64::from("inf");
    assert!(math.isinf(-(x)));
    x = f64::from("nan");
    assert!(math.isnan(-(x)));
    x = i32::from(100);
    assert!(-(x) == -100);
}

pub fn test_pos() {
    let mut x: i32 = 12;
    assert!(None(x) == 12);
    x = 1.1;
    assert!(None(x) as f64 == 1.1);
    x = 0.0;
    assert!(None(x) as f64 == 0.0);
    x = f64::from("inf");
    assert!(math.isinf(None(x)));
    x = None(f64::from("inf"));
    assert!(math.isinf(None(x)));
    x = f64::from("nan");
    assert!(math.isnan(None(x)));
    x = i32::from(100);
    assert!(None(x) == 100);
}

pub fn main() {
    test_bool_ops();
    test_bool_ops_lazy_eval();
    test_neg();
    test_pos();
    println!("{}", "OK");
}
