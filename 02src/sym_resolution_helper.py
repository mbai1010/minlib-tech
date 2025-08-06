# sym_resolution_helper.py
# symbol_info_table: { "libname.so": { "symbol": { "version": str or None } } }
# copy_reloc_symbols: { "libname.so": { "symbol": { "version": str or None } } }
# sym_to_lib_map: { "symbol": "libname.so" }  # no version info

import os
from elf_utils_helper import get_symbols, get_defined_symbols_from_archive, extract_defined_symbols_version, extract_copy_relocation_symbols, get_symbol_aliases_by_address

import config

sym_to_lib_map = {}

symbol_info_table = {}

copy_reloc_symbols = {}

addr_to_symbols = {}

# generate the table for symbols and its mapped library
def get_defined_symbol_map():
    """
    List the defined symbols of each shared library 
    """
    global sym_to_lib_map
    sym_to_lib_map.clear()
    for lib in config.SHARED_LIBRARIES:
        lib_path = lib.get("archive")
        print(f"[DEBUG] Processing archive: {lib_path}")
        symbols = get_defined_symbols_from_archive(lib_path)
        print(f"[DEBUG] Total symbols: {len(symbols)}")
        for sym in symbols:
            if sym in sym_to_lib_map:
                # print(f"[Warning] Symbol {sym} defined in multiple libraries: {sym_to_lib_map[sym]} and {lib['name']}")
                continue #follow the ld rule, first matched symbol win 
            sym_to_lib_map[sym] = lib["name"]
    
    print(f"[DEBUG] Total sym_to_lib_map: {len(sym_to_lib_map)}")
    return sym_to_lib_map

# find the symbols mapped library based on the table 
def resolve_undefined_symbols(undefined_set):
    resolved = {}
    for sym in undefined_set:
        if sym in sym_to_lib_map:
            resolved[sym] = sym_to_lib_map[sym]
    return resolved

# generate a table for each library that includes its symbols name, symbols version 
def populate_symbol_info_table():
    """
    Populate the global symbol_info_table using SHARED_LIBRARIES config.
    Each shared library's undefined symbols and versions are stored.
    """
    global symbol_info_table
    symbol_info_table.clear()
    for lib in config.SHARED_LIBRARIES:
        so_path = os.path.join(lib["path"], lib["name"])
        raw = extract_defined_symbols_version(so_path)

        # Wrap each symbol with version dict
        symbol_info_table[lib["name"]] = {
            sym: { "version": ver } for sym, ver in raw.items()
        }

# get the copy relocation data symbols from all the executable files, list the library, its copy reloc symbols, symbols version
def populate_copy_reloc_symbols():
    global copy_reloc_symbols
    copy_reloc_symbols.clear()

    all_copy_reloc_syms = set()
    for comp in config.COMPONENTS:
        exe_path = os.path.join(comp["path"], comp["name"])
        symbols = extract_copy_relocation_symbols(exe_path)
        all_copy_reloc_syms.update(symbols)

    for sym in all_copy_reloc_syms:
        provider = sym_to_lib_map.get(sym)
        if not provider:
            print(f"[WARN] Copy reloc symbol '{sym}' has no provider in SHARED_LIBRARIES")
            continue
        
        if provider not in copy_reloc_symbols:
            copy_reloc_symbols[provider] = {}

        version = symbol_info_table.get(provider, {}).get(sym, {}).get("version")
        copy_reloc_symbols[provider][sym] = { "version": version }

    return copy_reloc_symbols

def populate_addr_to_symbols():
    """
    Populates the global addr_to_symbols dictionary.
    Format:
      addr_to_symbols = {
          "libc.so": {
              0xdeadbeef: ["__environ", "environ", ...],
              ...
          },
          ...
      }
    """
    global addr_to_symbols
    addr_to_symbols.clear()

    for lib in config.SHARED_LIBRARIES:
        so_path = os.path.join(lib["path"], lib["name"])
        libname = os.path.basename(so_path)

        aliases = get_symbol_aliases_by_address(so_path)
        if not aliases:
            print(f"[WARN] No aliases found for {libname}")
            continue

        addr_to_symbols[libname] = aliases

def expand_symbols_with_aliases(symbols):
    """
    Given a symbol list like { 'environ': None }, return a new list including aliases
    """
    expanded = dict(symbols)
    known_symbols = set(symbols.keys())

    for sym in known_symbols:
        # Get the provider library (e.g., "libc.so")
        provider = sym_to_lib_map.get(sym)
        if not provider:
            print(f"[WARN] No provider found for symbol '{sym}' in sym_to_lib_map")
            continue

        addr_map = addr_to_symbols.get(provider)
        if not addr_map:
            print(f"[WARN] No addr-to-symbols map found for provider '{provider}'")
            continue

        # Find the address for this symbol
        addr = None
        for a, syms in addr_map.items():
            if sym in syms:
                addr = a
                break
        if addr is None:
            continue

        # Add all aliases at that address to the symbol list
        for alias in addr_map[addr]:
            if alias not in expanded:
                expanded[alias] = symbols[sym]  # preserve version info

    return expanded