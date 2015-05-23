use std::env;
use std::fs;
use std::io;
use std::path::Path;

fn get_platform() -> String {
    let features = env::vars().filter(|&(ref key, _)| key.starts_with("CARGO_FEATURE_"));
    let (feature_var, _) = features.last().expect("No platform specified");
    feature_var.trim_left_matches("CARGO_FEATURE_").to_string()
}

fn copy_linker_scripts<P: AsRef<Path>>(out_path: P) -> io::Result<()> {
    // Get the name of the MCU for which we're compiling
    let target = get_platform();

    // Try copying the linker scripts
    let target_dir = Path::new("src/hal").join(&target);
    let out_dir: &Path = out_path.as_ref();
    try!(fs::copy("src/hal/layout_common.ld", out_dir.join("layout_common.ld")));
    try!(fs::copy(target_dir.join("iomem.ld"), out_dir.join("iomem.ld")));
    try!(fs::copy(target_dir.join("layout.ld"), out_dir.join("layout.ld")));

    Ok(())
}

fn main() {
    let profile = env::var("PROFILE").unwrap();
    match profile.as_ref() {
        "dev" | "release" | "debug" => {},
        _ => {
            return;
        },
    }
    // Get output directory for cargo for zinc crate
    let out_dir = env::var("OUT_DIR").unwrap();

    // Move linker scripts to cargo output dir
    match copy_linker_scripts(&out_dir) {
        Ok(_) => {},
        Err(e) => panic!("Failed to copy linker scripts: {}", e)
    }

    // Make sure that the output dir is passed to linker
    println!("cargo:rustc-link-search=native={}", out_dir);
}
