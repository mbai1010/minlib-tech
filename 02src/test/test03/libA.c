#include <stdio.h>

void func1() {
    printf("func1\n");
}

void func2() {
    printf("func2\n");
}

void (*dispatch_table[])() = { func1, func2 };

