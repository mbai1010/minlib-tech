# rebuild_helper.py

import os
import subprocess

def _generate_version_script(symbols, output_path):
    with open(output_path, "w") as f:
        f.write("{\n  global:\n")
        for sym in symbols:
            f.write(f"    {sym};\n")
        f.write("  local: *;\n};\n")


def rebuild_shared_library(original_so_path, output_so_path, symbols):
    cflags = ["-fPIC", "-fno-plt", "-ffunction-sections", "-fdata-sections"]
    lib_dir = os.path.dirname(original_so_path)

    version_script_path = os.path.join(lib_dir, "version_script.vers")
    _generate_version_script(symbols, version_script_path)    
    
    # collect all .c files
    source_files = []
    for root, _, files in os.walk(lib_dir):
        for file in files:
            if file.endswith(".c"):
                source_files.append(os.path.join(root, file))

    if not source_files:
        raise FileNotFoundError(f"No .c files found in {lib_dir} or subdirectories to rebuild {output_so_path}")

    cmd = [
        "gcc",
        *cflags,
        *source_files,
        "-shared", "-Wl,--gc-sections",
        f"-Wl,--version-script={version_script_path}",
        "-o", output_so_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Build failed for {output_so_path}: {result.stderr}")

    return output_so_path

