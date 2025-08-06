# elf_utils_helper.py

from elftools.elf.elffile import ELFFile
from elftools.elf.constants import SHN_INDICES
from elftools.elf.gnuversions import GNUVerNeedSection,GNUVerDefSection
from elftools.elf.sections import StringTableSection
from elftools.elf.relocation import RelocationSection
from elftools.common.exceptions import ELFError

import os
import tempfile
import subprocess
import shutil
import config
from collections import defaultdict

def _get_symbol_section(elf):
    e_type = elf.header["e_type"]

    # ET_EXEC (2): executable
    # ET_DYN  (3): shared library or PIE executable
    if e_type == 'ET_EXEC':
        return elf.get_section_by_name(".dynsym")
    elif e_type == 'ET_DYN':
        # Prefer .symtab if available (for internal + global symbols)
        symtab = elf.get_section_by_name(".symtab")
        if symtab and symtab.num_symbols() > 0:
            return symtab
        return elf.get_section_by_name(".dynsym")

    # Fallback: return .symtab if present
    symtab = elf.get_section_by_name(".symtab")
    if symtab and symtab.num_symbols() > 0:
        return symtab

    return elf.get_section_by_name(".dynsym")

# ------------------------------------------------------------
# 2.  Extract **undefined** symbols (and optional version)
# ------------------------------------------------------------
from elftools.elf.gnuversions import GNUVerNeedSection

def extract_undefined_symbols_version(file_path):
    """
    Return dict { symbol_name: version_string | None } for every
    global/weak *undefined* symbol in .dynsym.
    Works even when the binary has no versioning sections.
    """
    versions = {}

    with open(file_path, "rb") as f:
        elf = ELFFile(f)

        dynsym      = elf.get_section_by_name(".dynsym")
        versym      = elf.get_section_by_name(".gnu.version")
        verneed_sec = elf.get_section_by_name(".gnu.version_r")

        if not dynsym:
            return versions

        # --------------------------------------------------
        # Helper tables (safe even if sections are missing)
        # --------------------------------------------------
        ver_indices     = []
        veridx_to_name  = {}

        if versym:
            ver_idx_data = versym.data()
            ver_indices = [
                int.from_bytes(ver_idx_data[i:i+2],
                               byteorder="little" if elf.little_endian else "big")
                for i in range(0, len(ver_idx_data), 2)
            ]

        if verneed_sec:
            try:
                strtab_idx     = dynsym["sh_link"]
                strtab_section = elf.get_section(strtab_idx)

                verneed = GNUVerNeedSection(
                    verneed_sec.header,
                    verneed_sec.name,
                    elf,
                    strtab_section
                )
                for verneed_entry, aux_iter in verneed.iter_versions():
                    for aux in aux_iter:
                        veridx_to_name[aux["vna_other"]] = aux.name
            except Exception as e:
                print(f"[WARN] Failed to parse version needs in {file_path}: {e}")

        # --------------------------------------------------
        # Walk the dynsym table
        # --------------------------------------------------
        for idx, sym in enumerate(dynsym.iter_symbols()):
            if (
                sym.name
                and sym["st_shndx"] == "SHN_UNDEF"
                and sym["st_info"]["bind"] in ("STB_GLOBAL", "STB_WEAK")
            ):
                version = None
                if idx < len(ver_indices):
                    veridx = ver_indices[idx]
                    if veridx not in (0, 1):
                        version = veridx_to_name.get(veridx)
                versions[sym.name] = version

    return versions


def extract_defined_symbols_version(provider_path):
    """
    Returns:
        dict: {symbol_name: version_string or None}
    """
    versions = {}
    with open(provider_path, "rb") as f:
        elf = ELFFile(f)

        dynsym = elf.get_section_by_name(".dynsym")
        versym = elf.get_section_by_name(".gnu.version")
        verdef_sec = elf.get_section_by_name(".gnu.version_d")

        if not dynsym:
            return versions

        ver_indices     = []
        veridx_to_name  = {}

        if versym:                                         # .gnu.version present
            ver_idx_data = versym.data()
            ver_indices = [
                int.from_bytes(ver_idx_data[i:i+2],
                               byteorder="little" if elf.little_endian else "big")
                for i in range(0, len(ver_idx_data), 2)
            ]

        if verdef_sec:                                    # .gnu.version_d present
            try:
                verdef = GNUVerDefSection(
                    verdef_sec.header,
                    verdef_sec.name,
                    elf,
                    elf.get_section(verdef_sec["sh_link"])
                )
                for verdef_entry, aux_iter in verdef.iter_versions():
                    for aux in aux_iter:
                        veridx_to_name[verdef_entry["vd_ndx"]] = aux.name
            except Exception as e:
                print(f"[WARN] Failed to parse version definitions in {provider_path}: {e}")

        for idx, sym in enumerate(dynsym.iter_symbols()):
            if (
                sym.name
                and sym["st_shndx"] != "SHN_UNDEF"
                and sym["st_info"]["bind"] in ("STB_GLOBAL", "STB_WEAK")
            ):
                version = None
                if idx < len(ver_indices):
                    veridx = ver_indices[idx]
                    if veridx not in (0, 1):        # 0 = local, 1 = global (unversioned)
                        version = veridx_to_name.get(veridx)
                versions[sym.name] = version

        return versions

def _extract_defined_symbols_from_relocatable(file_path):
    """
    Extract defined global/weak symbols from .symtab of a relocatable ELF file.
    """
    with open(file_path, "rb") as f:
        elf = ELFFile(f)
        defined = set()
        
        symtab = elf.get_section_by_name('.symtab')
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


# get symbol name and version from .so 
def get_symbols(file_path):
    undefined = extract_undefined_symbols_version(file_path)
    defined = extract_defined_symbols_version(file_path)

    return {
        "undefined": undefined,
        "defined": defined
    }

# get symbol name from .a, in some case, the symbol type in .so is t and in .a is U, 
# we follow the .a since we reuild the .so based on the object files from .a 
def get_defined_symbols_from_archive(archive_path):
    """
    Extracts all .o files from an archive (.a), analyzes each with get_symbols(),
    and returns a combined result.
    """
    all_defined = {}

    if not os.path.isfile(archive_path):
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    lib_entry = next((lib for lib in config.SHARED_LIBRARIES if lib["archive"] == archive_path), None)

    output_object = lib_entry["object"]
    temp_dir = os.path.join(os.path.dirname(output_object), "extracted_objs")

    for filename in os.listdir(temp_dir):
        obj_path = os.path.join(temp_dir, filename)
        if not is_relocatable(obj_path):
            continue
        try:
            defined_symbols = _extract_defined_symbols_from_relocatable(obj_path)
        except Exception as e:
            print(f"[WARN] Failed to read symbols from {filename}: {e}")
            continue
    
        for sym in defined_symbols:
            if sym not in all_defined:
                all_defined[sym] = None  # version not needed here

    return all_defined

def extract_copy_relocation_symbols(file_path):
    """
    Returns a set of symbol names that are involved in COPY relocations (R_X86_64_COPY).
    These symbols are global data objects that are copied from shared libraries into the executable.
    """
    copy_syms = set()

    with open(file_path, "rb") as f:
        elf = ELFFile(f)

        symtab = elf.get_section_by_name(".dynsym")
        if not symtab:
            return copy_syms

        # Map symbol index → symbol name
        idx_to_name = {i: sym.name for i, sym in enumerate(symtab.iter_symbols())}

        for section in elf.iter_sections():
            if not isinstance(section, RelocationSection):
                continue

            for reloc in section.iter_relocations():
                if reloc['r_info_type'] == 5:  # R_X86_64_COPY
                    sym_idx = reloc['r_info_sym']
                    sym_name = idx_to_name.get(sym_idx)
                    if sym_name:
                        copy_syms.add(sym_name)

    return copy_syms

#when we use relocation info to find the symbol, the executable may call a weak alias symbol, and the relocation info may save
#the strongest version of the symbol that is not the same name as the weak alias symbol, so we need to keep all the alias of the symbols  
def get_symbol_aliases_by_address(elf_path):
    """
    Returns a dict mapping address → [symbol1, symbol2, ...]
    """
    addr_to_symbols_map = defaultdict(list)

    with open(elf_path, "rb") as f:
        elf = ELFFile(f)
        dynsym = elf.get_section_by_name(".dynsym")
        if not dynsym:
            return {}

        for sym in dynsym.iter_symbols():
            if not sym.name:
                continue
            if sym['st_info']['bind'] not in ('STB_GLOBAL', 'STB_WEAK'):
                continue
            if sym['st_shndx'] == 'SHN_UNDEF':
                continue
            addr = sym['st_value']
            addr_to_symbols_map[addr].append(sym.name)

    return addr_to_symbols_map


def is_relocatable(file_path):
    try:
        with open(file_path, "rb") as f:
            magic = f.read(4)
            if magic != b'\x7fELF':
                print(f"[WARNING] Not an ELF file (invalid magic): {file_path}")
                return False
            f.seek(0)
            elf = ELFFile(f)
            return elf.header['e_type'] == 'ET_REL'
    except ELFError as e:
        print(f"[ERROR] Failed to parse ELF in file: {file_path} — {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error in file: {file_path} — {e}")
        return False

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
        
       # 4. Test undefined symbol versions
        try:
            versions = _extract_undefined_symbols_version(file_path)
            print(f"  [*] undefined symbol versions ({len(versions)}):")
            for sym, ver in list(versions.items())[:5]:
                print(f"      {sym}: {ver}")
        except Exception as e:
            print("  [!] _extract_undefined_symbols_version error:", e)

        # 5. Test defined symbol versions
        try:
            with open(file_path, "rb") as f:
                elf = ELFFile(f)
                def_versions = extract_defined_symbols_version(file_path)
                print(f"  [*] defined symbol versions ({len(def_versions)}):")
                for sym, ver in list(def_versions.items())[:5]:
                    print(f"      {sym}: {ver}")
        except Exception as e:
            print("  [!] extract_defined_symbols_version error:", e)

    # Require path to a .o file
    if len(sys.argv) != 2:
        print("Usage: python elf_utils_helper.py path/to/test.o")
        sys.exit(1)

    test_file = sys.argv[1]
    if not os.path.isfile(test_file):
        print(f"File does not exist: {test_file}")
        sys.exit(1)

    _run_test(test_file)
