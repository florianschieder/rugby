// Dynamic Library level

// This is only a primitive wrapper in this illustration, sometimes it may have
// to operate unsafely (pointers, ...) or do some type converting.

#[no_mangle]
pub extern "C" fn rugby_sum(lower_bound: u32, upper_bound: u32) -> u32 {
    sum(lower_bound, upper_bound)
}

// Rust level

fn sum(lower_bound: u32, upper_bound: u32) -> u32 {
    match lower_bound {
        0 | 1 => (upper_bound * (upper_bound + 1)) / 2,
        _ => sum(1, upper_bound) - sum(1, lower_bound - 1),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn works() {
        assert_eq!(55, sum(0, 10));
        assert_eq!(55, sum(1, 10));
        assert_eq!(54, sum(2, 10));
        assert_eq!(45, sum(5, 10));
        assert_eq!(19, sum(9, 10));
    }
}
