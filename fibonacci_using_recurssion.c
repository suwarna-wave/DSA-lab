#include <stdio.h>

// Global array for memoization
long int table[1005];

// Function to calculate Fibonacci using memoization
long int Fibo(int n) {
    if (n <= 0) {
        printf("Error: Fibonacci is not defined for n <= 0.\n");
        return 0;
    }
    if (n == 1 || n == 2) {
        return 1;
    }
    if (table[n] == -1) {
        table[n] = Fibo(n - 1) + Fibo(n - 2);
    }
    return table[n];
}

// Main function
int main() {
    long int result, n;
    int i;

    // Initialize memoization table
    for (i = 0; i < 1000; i++) {
        table[i] = -1;
    }

    printf("Enter a positive integer for Fibonacci: ");
    scanf("%ld", &n);

    result = Fibo(n);

    if (result != -1) {
        printf("The %ldth Fibonacci term is %ld.\n", n, result);
    }

    return 0;
}
