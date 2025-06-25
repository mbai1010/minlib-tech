#include <stdio.h>
    int shared_val_A = 10;

    void funcA() {
        printf("funcA from libA, val = %d\n", shared_val_A);
    }
