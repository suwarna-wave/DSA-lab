#include <stdio.h>
#include <stdlib.h>
#include <time.h>




// heapify function
void heapify(int arr[], int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    
    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }
    
    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }
    
    if (largest != i) {
        int temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;
        
        heapify(arr, n, largest);
    }
}




// build heap function
void build_heap(int arr[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }
}




// Heap sort function
void heap_sort(int arr[], int n) {
    build_heap(arr, n);
    
    for (int i = n - 1; i > 0; i--) {
        int temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;
        n=n-1;
        
        heapify(arr, i, n); 
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
    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("Invalid input. Please enter a positive integer.\n");
        return 1;
    }
    
    int *arr = (int *)malloc(n * sizeof(int));
    if (arr == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }
    
    srand(time(0));
    
    // Generate random array
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 100;
    }
    
    printf("Original array: ");
    printArray(arr, n);
    
    // Start time measurement
    start = clock();
    
    // Sort array calling heap sort
    heap_sort(arr, n);
    
    // End time measurement
    end = clock();
    
    printf("Sorted array: ");
    printArray(arr, n);
    
    // Calculate the time taken by the sort function
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken: %f seconds\n", cpu_time_used);
    
    free(arr);
    return 0;
}