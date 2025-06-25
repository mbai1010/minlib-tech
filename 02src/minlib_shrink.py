# shrink_helper.py

from sym_resolution_helper import (
    resolve_undefined_symbols
)
from rebuild_helper import rebuild_shared_library
import config
import os
from elf_utils_helper import get_symbols


def run_shrink_process(input_files, undefs=None):
    if undefs is None:
        undefs = set()

    # Step 1: Extract undefined symbols from input
    new_undefs = set()
    for f in input_files:
        symbols = get_symbols(f)
        new_undefs.update(symbols["undefined"])

    # Step 2: Check termination condition
    if new_undefs.issubset(undefs):
        return

    # Step 3: Update undefine symbol set 
    undefs |= new_undefs

    # Step 4: Map undefined symbols to providers
    symbol_provider_map = resolve_undefined_symbols(new_undefs)

    # Step 5: Group symbols by provider
    provider_symbols = {}
    for sym, provider in symbol_provider_map.items():
        provider_symbols.setdefault(provider, set()).add(sym)

    # Step 6: Rebuild each provider with minimal export
    next_inputs = []
    for provider, symbols in provider_symbols.items():
        lib_entry = next(lib for lib in config.SHARED_LIBRARIES if lib["name"] == provider)
        original_so = os.path.join(lib_entry["path"], provider)
        shrunk_so = os.path.join(lib_entry["path"], "shrunk_" + provider)

        rebuilt_so = rebuild_shared_library(
            original_so_path=original_so,
            output_so_path=shrunk_so,
            symbols=symbols
        )
        next_inputs.append(rebuilt_so)

    # Step 7: Recurse
    run_shrink_process(next_inputs, undefs)

