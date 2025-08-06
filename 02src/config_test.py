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
        "path": "./test/test01/libA/",
        "object": "./test/test01/libA/libA.o"
    },
    {
        "name": "libB.so",
        "path": "./test/test01/libB/",
        "object": "./test/test01/libB/libB.o"
    },
    {
        "name": "libC.so",
        "path": "./test/test01/libC/",
        "object": "./test/test01/libC/libC.o"
    }
]
