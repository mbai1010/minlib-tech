# shrink_helper.py

from sym_resolution_helper import resolve_undefined_symbols, symbol_info_table, copy_reloc_symbols, expand_symbols_with_aliases
from rebuild_helper import rebuild_shared_library
import config
import os
from elf_utils_helper import get_symbols, extract_undefined_symbols_version


def run_shrink_process(input_files, undefs=None):
    if undefs is None:
        undefs = {}  # Dict[str, Optional[str]]

    # Step 1: Extract undefined symbols from input
    print(f"[STEP] Analyzing {len(input_files)} input file(s) for undefined symbols...")
    new_undefs = {}
    for f in input_files:
        print(f"[INFO] Scanning: {f}")
        symbols = get_symbols(f)
        print(f"[INFO] Found {len(symbols['undefined'])} undefined symbols in {f}")
        for sym, ver in symbols["undefined"].items():
            if sym not in undefs:
                new_undefs[sym] = ver
        for s, v in sorted(new_undefs.items()):
            print(f"  [UNDEF] {s} (ver={v})")

    # Step 2: Check termination condition
    if set(new_undefs).issubset(undefs):
        print("[STOP] No new undefined symbols. Shrinking complete.")
        return

    # Step 3: Update undefined symbol set 
    undefs.update(new_undefs)
    print(f"[STEP] Total undefined symbols so far: {len(undefs)}")

    print("[STEP] Patching undefined symbols with version info from original shared libraries...")
  
    for sym in undefs:
        if undefs[sym] is not None:
            continue
        for provider, symbols in symbol_info_table.items():
            if sym in symbols:
                undefs[sym] = symbols[sym]["version"]
                print(f"  [PATCH] {sym} -> version {undefs[sym]}")
                break

    # Step 4: Map undefined symbols to providers
    print("[STEP] Resolving symbols to providers...")
    print(f"[DEBUG] Total undefined symbols to resolve: {len(undefs)}")
    symbol_provider_map = resolve_undefined_symbols(undefs)
    print(f"[INFO] Mapped {len(symbol_provider_map)} symbols to shared libraries")
    for sym, provider in symbol_provider_map.items():
        print(f"  [MAP] {sym} -> {provider}")

    # Step 5: Group symbols by provider, keeping version info
    provider_symbols = {}  # Dict[str, Dict[str, Optional[str]]]
    for sym, provider in symbol_provider_map.items():
        version = undefs.get(sym)
        provider_symbols.setdefault(provider, {})[sym] = version

    print("[DEBUG] Final symbol list for each provider:")
    for provider, symbols in provider_symbols.items():
        print(f"  Provider: {provider}")
        for sym, ver in sorted(symbols.items()):
            print(f"    [EXPORTED] {sym} (ver={ver})")


    # Step 6: Rebuild each provider with minimal export
    print(f"[STEP] Preparing to rebuild {len(provider_symbols)} shared libraries")
    next_inputs = []
    for provider, symbols in provider_symbols.items():
        print(f"[INFO] Processing provider: {provider}")
        lib_entry = next(lib for lib in config.SHARED_LIBRARIES if lib["name"] == provider)

        #add copy_reloc_symbols for version script
        extra = copy_reloc_symbols.get(provider, {})
        for sym, ver in extra.items():
            if sym not in symbols:
                symbols[sym] = ver
                print(f"    [COPY_RELOC] {sym} (ver={ver})")

        archive_path = lib_entry["archive"]
        merged_obj_path = lib_entry["object"]

        shrunk_so = os.path.join(lib_entry["path"], "shrunk_" + provider)
        print(f"[INFO] Rebuilding shared library: {shrunk_so}")

        symbols = expand_symbols_with_aliases(symbols)

        rebuilt_so = rebuild_shared_library(
            input_obj=merged_obj_path,
            output_so_path=shrunk_so,
            symbols=symbols  # Dict[str, Optional[str]]
        )

        print(f"[OK] Rebuilt library: {rebuilt_so}")
        next_inputs.append(shrunk_so)

    # Step 7: Recurse
    print("[STEP] Recursing shrink process...")
    run_shrink_process(next_inputs, undefs)


