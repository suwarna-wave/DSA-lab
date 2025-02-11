#include <iostream>
using namespace std;

int binarySearch(int arr[], int n, int target) {
    int left = 0;
    int right = n - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        // Check if target is present at mid
        if (arr[mid] == target)
            return mid;
            
        // If target greater, ignore left half
        if (arr[mid] < target)
            left = mid + 1;
            
        // If target is smaller, ignore right half
        else
            right = mid - 1;
    }
    
    // Target not present in array
    return -1;
}

int main() {
    int arr[] = {2, 3, 4, 10, 40, 50, 60, 70};
    int n = sizeof(arr) / sizeof(arr[0]);
    int target = 10;
    
    int result = binarySearch(arr, n, target);
    
    if (result == -1)
        cout << "Element not found in array";
    else
        cout << "Element found at index " << result;
        
    return 0;
}