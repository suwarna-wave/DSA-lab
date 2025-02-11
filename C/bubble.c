#include <stdio.h>
#include <stdlib.h>
#include <time.h>


//Sorting function
void bubble_sort(int arr[100001], int n) {
    for (int i = 0; i < n - 1; i++) {

        for (int j = 0; j < n - i - 1; j++) {
            
            if (arr[j] > arr[j + 1]) {
                
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}



//display function
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}



//main function
int main() {
    int n;
    clock_t start, end;
    double cpu_time_used;

    printf("Enter the number of elements: ");
    scanf("%d", &n);
    
    int arr[n];
    srand(time(0));
    
    // Generate random array
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 100;
    }
    
    printf("Original array: ");
    printArray(arr, n);
    
    // Start time measurement
    start = clock();
    
    // Sort array calling bubble sort
    bubble_sort(arr, n);
    
    // End time measurement
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    
    printf("Sorted array: ");
    printArray(arr, n);
    printf("Time taken: %f seconds\n", cpu_time_used);
    
    return 0;
}
