# config.py

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# List of component object files (input)
COMPONENTS = [
    {
        "name": "vsftpd",
        "path": os.path.join(BASE_DIR, "real_test/vsftpd/vsftpd-3.0.3")
    }
]

# List of original shared/static libraries to shrink
# Each entry includes:
# - name: logical name used during resolution
# - path: output folder for shrunk shared library
# - archive: path to the .a static library
# - object: path to the merged .o to be generated from .a
SHARED_LIBRARIES = [
    {
        "name": "libssl.so.3",
        "path": os.path.join(BASE_DIR, "test/test04/01ssl/"),
        "archive": os.path.join(BASE_DIR, "test/test04/01ssl/libssl.a"),
        "object": os.path.join(BASE_DIR, "test/test04/01ssl/libssl_custom.o")
    },
    {
        "name": "libcrypto.so.3",
        "path": os.path.join(BASE_DIR, "test/test04/02crypto/"),
        "archive": os.path.join(BASE_DIR, "test/test04/02crypto/libcrypto.a"),
        "object": os.path.join(BASE_DIR, "test/test04/02crypto/libcrypto_custom.o")
    },
    {
        "name": "libc.so.6",
        "path": os.path.join(BASE_DIR, "test/test04/01libc/"),
        "archive": os.path.join(BASE_DIR, "test/test04/01libc/libc.a"),
        "object": os.path.join(BASE_DIR, "test/test04/01libc/libc_custom.o")
    },
    {
        "name": "libcrypt.so.1",
        "path": os.path.join(BASE_DIR, "test/test04/02crypt/"),
        "archive": os.path.join(BASE_DIR, "test/test04/02crypt/libcrypt.a"),
        "object": os.path.join(BASE_DIR, "test/test04/02crypt/libcrypt_custom.o")
    }
]
