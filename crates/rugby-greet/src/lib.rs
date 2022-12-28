use std::ffi::{CStr, CString};
use std::os::raw::c_char;

// Dynamic Library level

#[no_mangle]
pub unsafe extern "C" fn rugby_greet(name: *const c_char) -> *const c_char {
    let unwrapped_name = unsafe { CStr::from_ptr(name) };
    let greeting = CString::new(greet(
        unwrapped_name.to_str().expect("should be a valid string"),
    ))
    .expect("should be a valid string");

    greeting.into_raw()
}

/// # Safety
/// The ptr should be a valid pointer to the string allocated by rust
#[no_mangle]
pub unsafe extern "C" fn free_string(ptr: *const c_char) {
    // Take the ownership back to rust and drop the owner
    let _ = CString::from_raw(ptr as *mut _);
}

// Rust level

fn greet(name: &str) -> String {
    format!("Hello {}!", name)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn works() {
        assert_eq!(String::from("Hello Developer!"), greet("Developer"));
    }
}
