# rebuild_helper.py

import os
import subprocess

def _generate_version_script(symbols, output_path):
    with open(output_path, "w") as f:
        f.write("{\n  global:\n")
        for sym in symbols:
            f.write(f"    {sym};\n")
        f.write("  local: *;\n};\n")


def rebuild_shared_library(input_obj, output_so_path, symbols):
    lib_dir = os.path.dirname(output_so_path)

    version_script_path = os.path.join(lib_dir, "version_script.vers")
    _generate_version_script(symbols, version_script_path)    
    
    #TBD: how to process link_cmd, as an input argument?
    default_cmd = [
        "gcc",
        "-shared", "-Wl,--gc-sections",
        f"-Wl,--version-script={version_script_path}",
        input_obj,
        "-o", output_so_path
    ]

    result = subprocess.run(default_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Build failed for {output_so_path}: {result.stderr}")

    return output_so_path

