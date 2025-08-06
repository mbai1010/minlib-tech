import os
import struct

def read_archive_members(filename, output_dir):
    with open(filename, 'rb') as f:
        magic = f.read(8)
        if magic != b"!<arch>\n":
            raise ValueError("Invalid archive format")

        index = 0
        while True:
            header_pos = f.tell()
            hdr = f.read(60)
            if len(hdr) < 60:
                break  # End of file

            # Parse header
            ar_name = hdr[0:16].decode('utf-8').strip()
            ar_size = int(hdr[48:58].decode('utf-8').strip())
            fmag = hdr[58:60]

            if fmag != b'`\n':
                raise ValueError("Invalid ar header separator")

            # Normalize filename
            name = ar_name.split('/')[0] or f"unnamed_{index}"

            # Read file content
            content = f.read(ar_size)

            # Save file with offset-based name
            output_name = f"{header_pos:08x}_{name}"
            output_path = os.path.join(output_dir, output_name)
            with open(output_path, 'wb') as out:
                out.write(content)

            index += 1

            # Skip padding byte if size is odd
            if ar_size % 2 == 1:
                f.read(1)

# Example usage
if __name__ == "__main__":
    archive_path = "libc.a"
    output_directory = "extracted_members"

    os.makedirs(output_directory, exist_ok=True)
    read_archive_members(archive_path, output_directory)
    print(f"Extracted to {output_directory}/")

