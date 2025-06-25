# config.py

# List of component object files (input)
# Each is a dict with: name and path
COMPONENTS = [
    {
        "name": "test1.o",
        "path": "./test/test01/"
    },
    {
        "name": "test2.o",
        "path": "./test/test01/"
    }
]

# List of original shared libraries
# Each is a dict with: name (logical name), path (absolute or relative .so path)
SHARED_LIBRARIES = [
    {
        "name": "libA.so",
        "path": "./test/test01/libA/"
    },
    {
        "name": "libB.so",
        "path": "./test/test01/libB/"
    },
    {
        "name": "libC.so",
        "path": "./test/test01/libC/"
    }
]
