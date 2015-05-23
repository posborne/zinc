use std::env;
use std::fs;
use std::io;
use std::path::Path;

fn copy_linker_scripts<P: AsRef<Path>>(out_path: P) -> io::Result<()> {
    // Get the name of the MCU for which we're compiling
    let target = env::var("TARGET").unwrap();

    // Try copying the linker scripts
    let target_dir = Path::new("src/hal").join(&target);
    let out_dir: &Path = out_path.as_ref();
    try!(fs::copy("src/hal/layout_common.ld", out_dir.join("layout_common.ld")));
    try!(fs::copy(target_dir.join("iomem.ld"), out_dir.join("iomem.ld")));
    try!(fs::copy(target_dir.join("layout.ld"), out_dir.join("layout.ld")));

    Ok(())
}

fn main() {
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
