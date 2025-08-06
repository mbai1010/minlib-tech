from minlib_shrink import run_shrink_process
import config
import os
from elf_utils_helper import is_relocatable, has_function_or_data_sections
from rebuild_helper import extract_and_merge_archive
from sym_resolution_helper import populate_symbol_info_table, get_defined_symbol_map, populate_copy_reloc_symbols, populate_addr_to_symbols


def main():
    # Step 0: sanity check of object files if they match our assumption (build with -ffunction-section -fdata-section -fPIC) or not
    # for lib in config.SHARED_LIBRARIES:
    #     input_obj = lib.get("object")
    #     if not input_obj or not os.path.isfile(input_obj):
    #         raise FileNotFoundError(f"Missing object file for {lib['name']}: {input_obj}")

    #     if not is_relocatable(input_obj):
    #         raise ValueError(f"{input_obj} is not a relocatable ELF file (ET_REL)")

    #     if not has_function_or_data_sections(input_obj):
    #         raise ValueError(
    #             f"{input_obj} does not contain .text.*, .data.*, .rodata.* sections. "
    #             "Please compile with -ffunction-sections and -fdata-sections!"
    #         )

    # Step 1: Collect component binary paths
    print("[INFO] Validating component input files...")
    component_paths = []
    for entry in config.COMPONENTS:
        path = os.path.join(entry["path"], entry["name"])
        if not os.path.isfile(path):
            raise FileNotFoundError(f"[ERROR] Component file not found: {path}")
        print(f"[OK] Component found: {path}")
        component_paths.append(path)
 
    # Step 2: extract and merge .o files from the .a into a single .o file
    for lib in config.SHARED_LIBRARIES:
        archive_path = lib["archive"]
        merged_obj_path = lib["object"]
        print(f"[INFO] Processing archive: {archive_path}")
        extract_and_merge_archive(archive_path, merged_obj_path)
        print(f"[OK] Merged object created: {merged_obj_path}")
    
    # Step 3: Prepare the mapping info of symbols name and version, we can initialze the version with none
    populate_symbol_info_table()

    # Step 4: get the symbol from the archive
    get_defined_symbol_map()

    # Step 5: copy relocation data symbol
    populate_copy_reloc_symbols()

    # Step 6: collect the alias of each symbol
    populate_addr_to_symbols()

    # Step 6: Begin shrink process
    print("[INFO] Starting shrink process...")
    run_shrink_process(input_files=component_paths)
    print("[DONE] Shrinking process completed.")

if __name__ == "__main__":
    main()
