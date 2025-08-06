import sys
import subprocess
import re

def count_symbols(lib_path):
    try:
        output = subprocess.check_output(["readelf", "-Ws", lib_path], text=True)
    except subprocess.CalledProcessError:
        print(f"Error reading symbols from {lib_path}")
        return 0, 0

    func_count = 0
    data_count = 0

    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 8:
            continue  # Not a valid symbol line

        type_field = parts[3]
        if type_field == "FUNC":
            func_count += 1
        elif type_field == "OBJECT":
            data_count += 1

    return func_count, data_count

def count_function_entries(lib_path):
    """
    Use objdump -d to count function entry points in .text section.
    """
    try:
        output = subprocess.check_output(["objdump", "-d", lib_path], text=True)
    except subprocess.CalledProcessError:
        print(f"Error disassembling {lib_path}")
        return 0

    function_entry_pattern = re.compile(r'^[0-9a-fA-F]+ <(.+)>:')
    count = 0

    for line in output.splitlines():
        if function_entry_pattern.match(line):
            count += 1

    return count

def get_section_sizes(lib_path):
    """
    Use readelf -SW to get .text and .data section sizes.
    """
    try:
        output = subprocess.check_output(["readelf", "-SW", lib_path], text=True)
    except subprocess.CalledProcessError:
        print(f"Error reading section headers from {lib_path}")
        return {}

    sizes = {}
    for line in output.splitlines():
        if ".text" in line or ".data" in line:
            parts = line.split()
            if ".text" in parts[1] or ".data" in parts[1]:
                section_name = parts[1]
                section_size = int(parts[5], 16)
                sizes[section_name] = section_size

    return sizes

def calculate_shrink_rate(original, shrunk):
    if original == 0:
        return 0.0
    return round((1 - shrunk / original) * 100, 2)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 comp_pair.py <original.so> <shrunk.so>")
        sys.exit(1)

    orig_path = sys.argv[1]
    shrunk_path = sys.argv[2]

    # Symbol counts
    orig_func, orig_data = count_symbols(orig_path)
    shrunk_func, shrunk_data = count_symbols(shrunk_path)


    func_sym_shrink = calculate_shrink_rate(orig_func, shrunk_func)
    data_sym_shrink = calculate_shrink_rate(orig_data, shrunk_data)

    print(f"{'TYPE':<20} {'ORIGINAL':>10} {'SHRUNK':>10} {'SHRINK RATE':>15}")
    print("-" * 60)
    print(f"{'FUNC Symbols':<20} {orig_func:>10} {shrunk_func:>10} {func_sym_shrink:>13}%")
    print(f"{'DATA Symbols':<20} {orig_data:>10} {shrunk_data:>10} {data_sym_shrink:>13}%")



if __name__ == "__main__":
    main()

