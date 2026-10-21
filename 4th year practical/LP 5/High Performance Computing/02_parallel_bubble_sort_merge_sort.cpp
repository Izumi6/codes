/*
 * ==============================================================================
 * LP-5 Practical 2: Parallel Bubble Sort and Merge Sort using OpenMP
 * 
 * Problem Statement:
 *   Write a program to implement Parallel Bubble Sort and Merge sort using OpenMP.
 *   Use existing algorithms and measure the performance of sequential and
 *   parallel algorithms.
 * 
 * How to Compile & Run:
 *   - On Windows (MinGW GCC):
 *       g++ -fopenmp 02_parallel_bubble_sort_merge_sort.cpp -o 02_parallel_bubble_sort_merge_sort.exe
 *       02_parallel_bubble_sort_merge_sort.exe
 * 
 *   - On Linux / Ubuntu:
 *       g++ -fopenmp 02_parallel_bubble_sort_merge_sort.cpp -o 02_parallel_bubble_sort_merge_sort
 *       ./02_parallel_bubble_sort_merge_sort
 * ==============================================================================
 */

#include <iostream>
#include <vector>
#include <cstdlib>
#include <iomanip>

#if defined(__has_include)
  #if __has_include(<omp.h>)
    #include <omp.h>
  #else
    #include <chrono>
    inline double omp_get_wtime() {
        return std::chrono::duration<double>(std::chrono::high_resolution_clock::now().time_since_epoch()).count();
    }
  #endif
#else
  #include <omp.h>
#endif

using namespace std;

// -------------------------------------------------------------
// 1. Sequential Bubble Sort
// -------------------------------------------------------------
void sequentialBubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

// -------------------------------------------------------------
// 2. Parallel Bubble Sort (Odd-Even Transposition Sort)
// -------------------------------------------------------------
void parallelBubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int phase = 0; phase < n; phase++) {
        // Even phase: compare elements at even indices (0, 2, 4...)
        if (phase % 2 == 0) {
            #pragma omp parallel for
            for (int i = 0; i < n - 1; i += 2) {
                if (arr[i] > arr[i + 1]) {
                    swap(arr[i], arr[i + 1]);
                }
            }
        }
        // Odd phase: compare elements at odd indices (1, 3, 5...)
        else {
            #pragma omp parallel for
            for (int i = 1; i < n - 1; i += 2) {
                if (arr[i] > arr[i + 1]) {
                    swap(arr[i], arr[i + 1]);
                }
            }
        }
    }
}

// -------------------------------------------------------------
// Merge Helper Function
// -------------------------------------------------------------
void merge(vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    vector<int> L(n1), R(n2);
    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

// -------------------------------------------------------------
// 3. Sequential Merge Sort
// -------------------------------------------------------------
void sequentialMergeSort(vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        sequentialMergeSort(arr, left, mid);
        sequentialMergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

// -------------------------------------------------------------
// 4. Parallel Merge Sort using OpenMP Sections
// -------------------------------------------------------------
void parallelMergeSort(vector<int>& arr, int left, int right, int depth = 0) {
    if (left < right) {
        int mid = left + (right - left) / 2;

        // Parallelize left and right recursive calls for initial levels
        if (depth < 4) {
            #pragma omp parallel sections
            {
                #pragma omp section
                parallelMergeSort(arr, left, mid, depth + 1);

                #pragma omp section
                parallelMergeSort(arr, mid + 1, right, depth + 1);
            }
        } else {
            sequentialMergeSort(arr, left, mid);
            sequentialMergeSort(arr, mid + 1, right);
        }
        merge(arr, left, mid, right);
    }
}

// Helper to print array elements
void printArray(const vector<int>& arr, int limit = 10) {
    int count = min((int)arr.size(), limit);
    for (int i = 0; i < count; i++) {
        cout << arr[i] << " ";
    }
    if ((int)arr.size() > limit) cout << "... (" << arr.size() << " total)";
    cout << endl;
}

int main() {
    // Small demonstration to show sorting works
    vector<int> demo = {64, 34, 25, 12, 22, 11, 90, 88, 45, 50};
    cout << "Original Small Array: ";
    printArray(demo);

    vector<int> demoBubble = demo;
    parallelBubbleSort(demoBubble);
    cout << "Bubble Sorted Array : ";
    printArray(demoBubble);

    vector<int> demoMerge = demo;
    parallelMergeSort(demoMerge, 0, demoMerge.size() - 1);
    cout << "Merge Sorted Array  : ";
    printArray(demoMerge);
    cout << endl;

    // Performance Comparison on larger arrays
    int nBubble = 5000;
    int nMerge = 50000;

    vector<int> arrBubble1(nBubble), arrMerge1(nMerge);
    for (int i = 0; i < nBubble; i++) arrBubble1[i] = rand() % 10000;
    for (int i = 0; i < nMerge; i++)  arrMerge1[i]  = rand() % 100000;

    vector<int> arrBubble2 = arrBubble1;
    vector<int> arrMerge2  = arrMerge1;

    cout << "--- Bubble Sort Performance (N = " << nBubble << ") ---" << endl;
    double start = omp_get_wtime();
    sequentialBubbleSort(arrBubble1);
    double end = omp_get_wtime();
    cout << "Sequential Bubble Sort Time: " << fixed << setprecision(4) << (end - start) << " seconds" << endl;

    start = omp_get_wtime();
    parallelBubbleSort(arrBubble2);
    end = omp_get_wtime();
    cout << "Parallel Bubble Sort Time  : " << fixed << setprecision(4) << (end - start) << " seconds" << endl;

    cout << "\n--- Merge Sort Performance (N = " << nMerge << ") ---" << endl;
    start = omp_get_wtime();
    sequentialMergeSort(arrMerge1, 0, arrMerge1.size() - 1);
    end = omp_get_wtime();
    cout << "Sequential Merge Sort Time : " << fixed << setprecision(4) << (end - start) << " seconds" << endl;

    start = omp_get_wtime();
    parallelMergeSort(arrMerge2, 0, arrMerge2.size() - 1);
    end = omp_get_wtime();
    cout << "Parallel Merge Sort Time   : " << fixed << setprecision(4) << (end - start) << " seconds" << endl;

    return 0;
}

/*
============================== SAMPLE OUTPUT ==============================
Original Small Array: 64 34 25 12 22 11 90 88 45 50 
Bubble Sorted Array : 11 12 22 25 34 45 50 64 88 90 
Merge Sorted Array  : 11 12 22 25 34 45 50 64 88 90 

--- Bubble Sort Performance (N = 5000) ---
Sequential Bubble Sort Time: 0.0140 seconds
Parallel Bubble Sort Time  : 0.1150 seconds

--- Merge Sort Performance (N = 50000) ---
Sequential Merge Sort Time : 0.0039 seconds
Parallel Merge Sort Time   : 0.0022 seconds
===========================================================================
*/
