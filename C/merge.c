#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to display the array
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Merge function
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1; // Size of the left subarray
    int n2 = r - m;     // Size of the right subarray

    // Create temporary arrays
    int L[n1], R[n2];

    // Copy data to temporary arrays
    for (int i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    // Merge the temporary arrays back into the original array
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of L[], if any
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copy the remaining elements of R[], if any
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

// Merge sort function
void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;

        // Sort first and second halves
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);

        // Merge the sorted halves
        merge(arr, l, m, r);
    }
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

    // Generate random array
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 100;
    }

    printf("Original array: ");
    printArray(arr, n);

    // Start time measurement
    start = clock();

    // Sort array using merge sort
    mergeSort(arr, 0, n - 1);

    // End time measurement
    end = clock();
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("Sorted array: ");
    printArray(arr, n);
    printf("Time taken: %f seconds\n", cpu_time_used);

    return 0;
}
