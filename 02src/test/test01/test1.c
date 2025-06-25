extern void funcA();
    extern int shared_val_B;

    int main() {
        funcA();
        return shared_val_B;
    }