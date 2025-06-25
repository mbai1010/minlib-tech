# elf_utils_helper.py

import subprocess
import re

def run_nm(file_path):
    result = subprocess.run(["nm", "-g", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"nm failed on {file_path}: {result.stderr}")
    return result.stdout

def run_readelf(file_path):
    result = subprocess.run(["readelf", "-Ws", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"readelf failed on {file_path}: {result.stderr}")
    return result.stdout

def extract_undefined_symbols_from_nm(nm_output):
    undefined = set()
    for line in nm_output.splitlines():
        if " U " in line:
            parts = line.strip().split()
            undefined.add(parts[-1])
    return undefined

def extract_defined_symbols_from_nm(nm_output):
    defined = set()
    for line in nm_output.splitlines():
        if re.search(r" [TDABCDG] ", line):
            parts = line.strip().split()
            defined.add(parts[-1])
    return defined

def get_symbols(file_path):
    nm_out = run_nm(file_path)
    return {
        "undefined": extract_undefined_symbols_from_nm(nm_out),
        "defined": extract_defined_symbols_from_nm(nm_out)
    }

