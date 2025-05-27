#include<stdio.h>

void greet();
int add(int a, int b);
void print_sum(int result);

int main() {
    greet();
    int x = 5;
    int y = 10;
    int result = add(x, y);
    print_sum(result);
    return 0;
}

void greet() {
    printf("Welcome to the program!\n");
}

int add(int a, int b) {
    return a + b;
}

void print_sum(int result) {
    printf("The sum is: %d\n", result);
}
