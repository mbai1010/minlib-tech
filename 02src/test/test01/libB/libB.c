#include <stdio.h>
    extern int shared_val_C; // from libC
    int shared_val_B = 20;

    void funcB() {
        printf("funcB from libB, val = %d\n", shared_val_C);
    }
   
