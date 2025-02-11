#include <stdio.h>

// Function to solve the Tower of Hanoi puzzle using recursion
void towerOfHanoi(int n, char src, char temp, char dist) {
    if (n == 1) {
        // Base case: Move a single disk from src to dist
        printf("Move disk 1 from %c to %c\n", src, dist);
        return;
    }
    
    // Move n-1 disks from src to temp (using dist as temporary storage)
    towerOfHanoi(n - 1, src, dist, temp);
    
    // Move the nth disk from src to dist
    printf("Move disk %d from %c to %c\n", n, src, dist);
    
    // Move n-1 disks from temp to dist (using src as temporary storage)
    towerOfHanoi(n - 1, temp, src, dist);
}

int main() {
    int n;
    
    // Input number of disks
    printf("Enter the number of disks: ");
    scanf("%d", &n);
    
    // Call the function to solve the Tower of Hanoi puzzle
    printf("The sequence of moves for %d disks is:\n", n);
    towerOfHanoi(n, 'A', 'B', 'C');  // A = source, B = temporary, C = destination
    
    return 0;
}
