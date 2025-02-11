#include <stdio.h>

// Function to calculate factorial using recursion
unsigned long long factorial(int n) {
    if (n == 0) {                            //0! = 1
        return 1;
    } else {
        return n * factorial(n - 1);         //recursion : n! = n * (n-1)!
    }
}

int main() {
    int num;
    printf("Enter a number: ");
    scanf("%d", &num);

    if (num < 0) {
        printf("Factorial of a negative number doesn't exist.\n");
    } else {
        printf("Factorial of %d is %llu\n", num, factorial(num));
    }

    return 0;
}