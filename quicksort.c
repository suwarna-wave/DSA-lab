#include <stdio.h>
#include <stdlib.h>
#include <time.h>


// Partition function
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    
    return i + 1;
}


// Quicksort function
void quick_sort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        
        quick_sort(arr, low, pi - 1);
        quick_sort(arr, pi + 1, high);
    }
}



// Display function
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}



// Main function
int main() {
    int n;
    clock_t start, end;
    double cpu_time_used;

    printf("Enter the number of elements: ");
    scanf("%d", &n);
    
    int arr[n];
    srand(time(0));
    
    // Generate random array with no upper limit
    for (int i = 0; i < n; i++) {
        arr[i] = rand();
    }
    
    printf("Original array: ");
    printArray(arr, n);
    
    // Start time measurement
    start = clock();
    
    // Sort array using quicksort
    quick_sort(arr, 0, n - 1);
    
    // End time measurement
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    
    printf("Sorted array: ");
    printArray(arr, n);
    printf("Time taken: %f seconds\n", cpu_time_used);
    
    return 0;
}
