# elf_utils_helper.py

from elftools.elf.elffile import ELFFile
from elftools.elf.constants import SHN_INDICES
import os

def _extract_undefined_symbols_from_elf(elf):
    undefined = set()
    symtab = elf.get_section_by_name(".symtab")
    if symtab is None:
        return undefined

    for sym in symtab.iter_symbols():
        # Since only global or weak are externally visible, 
        # we filter only defined STB_GLOBAL or STB_WEAK symbolss
        if (
            sym.name
            and sym['st_shndx'] == 'SHN_UNDEF'
            and sym['st_info']['bind'] in ('STB_GLOBAL', 'STB_WEAK')
        ):            
            undefined.add(sym.name)
    return undefined

def _extract_defined_symbols_from_elf(elf):
    defined = set()
    symtab = elf.get_section_by_name(".symtab")
    if symtab is None:
        return defined

    for sym in symtab.iter_symbols():
        if (
            sym.name
            and sym['st_shndx'] != 'SHN_UNDEF'
            and sym['st_info']['bind'] in ('STB_GLOBAL', 'STB_WEAK')
        ):
            defined.add(sym.name)
    return defined

def get_symbols(file_path):
    with open(file_path, "rb") as f:
        elf = ELFFile(f)
        return {
            "undefined": _extract_undefined_symbols_from_elf(elf),
            "defined": _extract_defined_symbols_from_elf(elf)
        }

def is_relocatable(file_path):
    with open(file_path, "rb") as f:
        elf = ELFFile(f)
        return elf.header['e_type'] == 'ET_REL'

def has_function_or_data_sections(file_path):
    with open(file_path, "rb") as f:
        elf = ELFFile(f)
        for section in elf.iter_sections():
            name = section.name
            if (
                name.startswith(".text.") or
                name.startswith(".data.") or
                name.startswith(".rodata.") or
                name.startswith(".bss.")
            ):
                return True
        return False


if __name__ == "__main__":
    import sys

    def _run_test(file_path):
        print(f"Testing ELF analysis on: {file_path}")

        # 1. Check relocatable
        try:
            print("  [*] is_relocatable:", is_relocatable(file_path))
        except Exception as e:
            print("  [!] is_relocatable error:", e)

        # 2. Check for section-splitting
        try:
            print("  [*] has_function_or_data_sections:", has_function_or_data_sections(file_path))
        except Exception as e:
            print("  [!] has_function_or_data_sections error:", e)

        # 3. Extract symbols
        try:
            symbols = get_symbols(file_path)
            print(f"  [*] defined symbols ({len(symbols['defined'])}):", sorted(list(symbols['defined']))[:5], "...")
            print(f"  [*] undefined symbols ({len(symbols['undefined'])}):", sorted(list(symbols['undefined']))[:5], "...")
        except Exception as e:
            print("  [!] get_symbols error:", e)

    # Require path to a .o file
    if len(sys.argv) != 2:
        print("Usage: python elf_utils_helper.py path/to/test.o")
        sys.exit(1)

    test_file = sys.argv[1]
    if not os.path.isfile(test_file):
        print(f"File does not exist: {test_file}")
        sys.exit(1)

    _run_test(test_file)
