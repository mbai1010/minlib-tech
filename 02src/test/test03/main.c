extern void (*dispatch_table[])();

int main() {
    dispatch_table[0]();  // indirect call to func1
    dispatch_table[1]();  // indirect call to func2
    return 0;
}

