extern void funcB();
    extern int shared_val_C;

    void call() {
        funcB();
        int temp = shared_val_C;
    }