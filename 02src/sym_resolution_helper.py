# sym_resolution_helper.py

import os
from elf_utils_helper import get_symbols
import config


def extract_component_undefined_symbols():
    all_undefs = set()
    for comp in config.COMPONENTS:
        file_path = os.path.join(comp["path"], comp["name"])
        symbols = get_symbols(file_path)
        all_undefs.update(symbols["undefined"])
    return all_undefs


def get_defined_symbol_map():
    """
    List the defined symbols of each shared library 
    """
    sym_to_lib_map = {}
    for lib in config.SHARED_LIBRARIES:
        lib_path = os.path.join(lib["path"], lib["name"])
        symbols = get_symbols(lib_path)
        for sym in symbols["defined"]:
            if sym in sym_to_lib_map:
                print(f"[Warning] Symbol {sym} defined in multiple libraries: {sym_to_lib_map[sym]} and {lib['name']}")
            sym_to_lib_map[sym] = lib["name"]
    return sym_to_lib_map


def resolve_undefined_symbols(undefined_set, sym_to_lib_map):
    resolved = {}
    for sym in undefined_set:
        if sym in sym_to_lib_map:
            resolved[sym] = sym_to_lib_map[sym]
    return resolved

