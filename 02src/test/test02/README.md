# MinLib Test Case: Function and Global Data Resolution

This test case is designed to validate the MinLib symbol resolution and shrinking using both **functions** and **global data** symbols across executable file and shared libraries.

## 🗂️ Directory Structure

```
minlib_test/
├── test/test01/
│   ├── test1.c          # Uses funcA() and shared_val_B
│   ├── test2.c          # Uses funcB() and shared_val_C
│   ├── libA/libA.c      # Defines funcA(), shared_val_A
│   ├── libB/libB.c      # Defines funcB(), shared_val_B and uses funcC()
│   └── libC/libC.c      # Defines funcC(), shared_val_C
```

## 🧪 Test Objective

This test checks whether:
- MinLib correctly extracts **undefined function and data symbols** from component object files.
- These undefined symbols are accurately **mapped to the original shared libraries**.
- Each shared library can be **rebuilt with version scripts and garbage collection** to include only required symbols.
- **Transitive dependencies** (e.g., `funcB` in libB needing `shared_val_C` from libC) are retained during rebuild.

## 🔍 Symbol Flow Example

- `test1.c` → needs `funcA()` (from libA) and `shared_val_B` (from libB)
- `test2.c` → needs `funcB()` (from libB), which itself uses `shared_val_C` (from libC)

## 🧰 How to Use

1. Compile each `.c` file into object files and shared libraries using:
    gcc -fPIE -fno-plt -c test1.c -o test1.o
    gcc -fPIE -fno-plt -c test2.c -o test2.o
    
    gcc -fPIC -fno-plt -c libA/libA.c -o libA.o
    gcc -shared -o libA.so libA.o

    gcc -fPIC -fno-plt -c libB/libB.c -o libB.o
    gcc -shared -o libB.so libB.o -L. -lC

    gcc -fPIC -fno-plt -c libC/libC.c -o libC.o
    gcc -shared -o libC.so libC.o
    ```

2. Run MinLib script to:
   - Extract undefined symbols
   - Map and track dependencies
   - Shrink libraries iteratively

3. Ensure:
   - `libA.so` includes `funcA` and `shared_val_A`
   - `libB.so` includes `funcB`, `shared_val_B'
   - `libC.so` includes only `funcC
