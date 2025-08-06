# config.py

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# List of component object files (input)
COMPONENTS = [
    {
        "name": "vsftpd",
        "path": "test/test04//vsftpd-3.0.3"
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
        "path": os.path.join(BASE_DIR, "test/test04/01ssl_new/"),
        "archive": os.path.join(BASE_DIR, "test/test04/01ssl_new/libssl.a"),
        "object": os.path.join(BASE_DIR, "test/test04/01ssl_new/libssl_custom.o")
    },
    {
        "name": "libcrypt.so.2.0.0",
        "path": os.path.join(BASE_DIR, "test/test04/02crypt_new/"),
        "archive": os.path.join(BASE_DIR, "test/test04/02crypt_new/libcrypt.a"),
        "object": os.path.join(BASE_DIR, "test/test04/02crypt_new/libcrypt_custom.o")
    },
    {
        "name": "libcrypto.so.3",
        "path": os.path.join(BASE_DIR, "test/test04/02crypto_new/"),
        "archive": os.path.join(BASE_DIR, "test/test04/02crypto_new/libcrypto.a"),
        "object": os.path.join(BASE_DIR, "test/test04/02crypto_new/libcrypto_custom.o")
    },
    {
        "name": "libc.so",
        "path": os.path.join(BASE_DIR, "test/test04/04musl_libc/"),
        "archive": os.path.join(BASE_DIR, "test/test04/04musl_libc/libc.a"),
        "object": os.path.join(BASE_DIR, "test/test04/04musl_libc/libc_custom.o")
    }
]
