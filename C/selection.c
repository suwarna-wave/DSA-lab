#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void selection_sort(int arr[100001], int n) {
    for (int i = 0; i < n - 1; i++) {
        int min = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[min]) {
                min = j;
            }
        }
        int temp = arr[min];
        arr[min] = arr[i];
        arr[i] = temp;
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
    
    int *arr = (int *)malloc(n * sizeof(int));
    if (arr == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }
    srand(time(0));
    
    // Generate random array
    for (int i = 0; i < n; i++) {
        arr[i] = rand();
    }
    
    printf("Original array: ");
    printArray(arr, n);
    
    // Start time measurement
    start = clock();
    
    // Sort array calling selection sort
    selection_sort(arr, n);
    
    // End time measurement
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    
    free(arr);
    return 0;
    printArray(arr, n);
    printf("Time taken: %f seconds\n", cpu_time_used);
    
    return 0;
}
