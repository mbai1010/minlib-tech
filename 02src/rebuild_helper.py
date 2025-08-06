# rebuild_helper.py

import os
import subprocess
from collections import defaultdict
from elf_utils_helper import is_relocatable
from archive_helper import read_archive_members
import sys
import shutil

# def _generate_version_script(symbols, output_path, version="OPENSSL_3.0.0"):
#     print(f"[DEBUG] Generating version script at: {output_path}")
#     print(f"[DEBUG] Total {len(symbols)} symbols to export:")
#     for sym in sorted(symbols):
#         print(f"  [EXPORT] {sym}")
    
#     with open(output_path, "w") as f:
#         f.write(f"{version} {{\n  global:\n")
#         for sym in symbols:
#             f.write(f"    {sym};\n")
#         f.write("  local: *;\n};\n")

# rebuild_helper.py
def _generate_version_script(symbols_with_versions, output_path):
    """
    Generate a version script based on symbol → version mappings.

    Args:
        symbols_with_versions: Dict[str, Optional[str]] – symbol name → version (or None)
        output_path: str – path to write the version script
    """
    version_map = defaultdict(list)
    for sym, ver in symbols_with_versions.items():
        if isinstance(ver, dict):
            version = ver.get("version", None)
        else:
            version = ver

        version_key = version if version else "DEFAULT"
        version_map[version_key].append(sym)

    wrote_default = False

    with open(output_path, "w") as f:
        for version, syms in version_map.items():
            f.write(f"{version} {{\n")
            f.write("  global:\n")
            for sym in sorted(syms):
                f.write(f"    {sym};\n")
            if version == "DEFAULT":
                f.write("  local: *;\n")
                wrote_default = True
            f.write("};\n\n")

        # If no DEFAULT block was written, write one just for `local: *;`
        if not wrote_default:
            f.write("DEFAULT {\n")
            f.write("  local: *;\n")
            f.write("};\n\n")



def extract_and_merge_archive(input_archive, output_object):
    # Use output_object's directory for temp extraction
    temp_dir = os.path.join(os.path.dirname(output_object), "extracted_objs")

    # ----- make sure the directory is clean -------------
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    # Extract all .o files
    read_archive_members(input_archive, temp_dir)

    # Identify relocatable objects
    obj_files = []
    non_relocatable = []

    for fname in os.listdir(temp_dir):
        fpath = os.path.join(temp_dir, fname)
        if is_relocatable(fpath):
            obj_files.append(fpath)
        else:
            non_relocatable.append(fpath)

    if non_relocatable:
        print(f"[WARNING] Found {len(non_relocatable)} non-relocatable files in archive '{input_archive}':", file=sys.stderr)
        for path in non_relocatable:
            print(f"  - {os.path.basename(path)}", file=sys.stderr)

    if not obj_files:
        raise RuntimeError(f"No relocatable object files found in archive '{input_archive}'.")
            
    subprocess.run(["ld", "-r", "-o", output_object] + obj_files, check=True)

    return output_object

def rebuild_shared_library(input_obj, output_so_path, symbols):
    lib_dir = os.path.dirname(output_so_path)

    version_script_path = os.path.join(lib_dir, "version_script.vers")
    _generate_version_script(symbols, version_script_path)    
    
    #TBD: how to process link_cmd, as an input argument?
    # default_cmd = [
    #     "musl-gcc",
    #     "-nostdinc", "-ffreestanding", "-nostartfiles", "-fPIC","-ffunction-sections","-fdata-sections"
    #     "-shared", "-Wl,--gc-sections",
    #     f"-Wl,--version-script={version_script_path}",
    #     input_obj,
    #     "-o", output_so_path
    # ]

    default_cmd = [
    "musl-gcc",
    "-nostdinc", "-nostdlib","-nostartfiles", "-ffreestanding",
    "-fPIC", "-fno-plt",
    "-shared", "-Wl,-z,now",
    "-Wl,--gc-sections",
    f"-Wl,--version-script={version_script_path}",
    input_obj,
    "-o", output_so_path
]

    result = subprocess.run(default_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Build failed for {output_so_path}: {result.stderr}")

    return output_so_path

