# elf_utils_helper.py

import subprocess
import re

def _run_nm(file_path):
    result = subprocess.run(["nm", "-g", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"nm failed on {file_path}: {result.stderr}")
    return result.stdout

def _run_readelf(file_path):
    result = subprocess.run(["readelf", "-Ws", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"readelf failed on {file_path}: {result.stderr}")
    return result.stdout

def _extract_undefined_symbols_from_nm(nm_output):
    undefined = set()
    for line in nm_output.splitlines():
        if " U " in line:
            parts = line.strip().split()
            undefined.add(parts[-1])
    return undefined

def _extract_defined_symbols_from_nm(nm_output):
    defined = set()
    for line in nm_output.splitlines():
        if re.search(r" [TDABCDG] ", line):
            parts = line.strip().split()
            defined.add(parts[-1])
    return defined

def get_symbols(file_path):
    nm_out = _run_nm(file_path)
    return {
        "undefined": _extract_undefined_symbols_from_nm(nm_out),
        "defined": _extract_defined_symbols_from_nm(nm_out)
    }

