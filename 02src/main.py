from minlib_shrink import run_shrink_process
import config
import os
from elf_utils_helper import is_relocatable, has_function_or_data_sections


def main():
    # Step 0: sanity check of object files if they match our assumption (build with -ffunction-section -fdata-section -fPIC) or not
    for lib in config.SHARED_LIBRARIES:
        input_obj = lib.get("object")
        if not input_obj or not os.path.isfile(input_obj):
            raise FileNotFoundError(f"Missing object file for {lib['name']}: {input_obj}")

        if not is_relocatable(input_obj):
            raise ValueError(f"{input_obj} is not a relocatable ELF file (ET_REL)")

        if not has_function_or_data_sections(input_obj):
            raise ValueError(
                f"{input_obj} does not contain .text.*, .data.*, .rodata.* sections. "
                "Please compile with -ffunction-sections and -fdata-sections!"
            )

    # Step 1: Collect component binary paths
    component_paths = [
        os.path.join(entry["path"], entry["name"])
        for entry in config.COMPONENTS
    ]
 
     # Step 2: Begin shrink process
    run_shrink_process(input_files=component_paths)


if __name__ == "__main__":
    main()
