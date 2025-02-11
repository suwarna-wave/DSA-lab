#include <stdio.h>

int binarySearch(int arr[], int size, int target) {
    int left = 0;
    int right = size - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        // If target is found at mid, return the index
        if (arr[mid] == target)
            return mid;

        // If target is greater, ignore left half
        if (arr[mid] < target)
            left = mid + 1;

        // If target is smaller, ignore right half
        else
            right = mid - 1;
    }

    // Target not found
    return -1;
}

int main() {
    int arr[] = {2, 3, 4, 10, 40, 50, 60, 70};
    int size = sizeof(arr) / sizeof(arr[0]);
    int target = 10;

    int result = binarySearch(arr, size, target);
    
    if (result == -1)
        printf("Element not found in array\n");
    else
        printf("Element found at index %d\n", result);

    return 0;
}