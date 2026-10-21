/**
 * ======================================================================================
 *   Laboratory Practice 5 (LP 5): High Performance Computing (410250)
 *   Practical 2: Parallel Bubble Sort and Merge Sort using OpenMP
 * ======================================================================================
 * 
 *   Problem Statement:
 *     Write a program to implement Parallel Bubble Sort and Merge sort using OpenMP.
 *     Use existing algorithms and measure the performance of sequential and parallel
 *     algorithms.
 * 
 *   Approach:
 *     1. Sequential Bubble Sort:
 *        - Standard O(n^2) comparison-based sorting.
 *     2. Parallel Bubble Sort (Odd-Even Transposition Sort):
 *        - Iterates over odd and even phases:
 *          * Even Phase: Compares and swaps adjacent elements at even indices (i, i+1).
 *          * Odd Phase : Compares and swaps adjacent elements at odd indices (i, i+1).
 *        - Both phases are parallelized across threads using #pragma omp parallel for.
 *     3. Sequential Merge Sort:
 *        - Divide-and-conquer O(n log n) sorting.
 *     4. Parallel Merge Sort:
 *        - Recursive divide-and-conquer using OpenMP tasks (#pragma omp task).
 *        - Left and right sub-arrays are processed concurrently by separate worker threads
 *          when sub-array size exceeds a cutoff threshold (to avoid task-spawning overhead).
 *     5. Performance Measurement:
 *        - Benchmarks execution time of both algorithms on identical random datasets.
 *        - Calculates and displays speedup = (T_sequential / T_parallel).
 * 
 *   Compilation Commands:
 *     - Linux (GCC):
 *         g++ -O2 -fopenmp 02_parallel_bubble_sort_merge_sort.cpp -o 02_parallel_bubble_sort_merge_sort
 *     - macOS (Apple Clang with Homebrew libomp):
 *         clang++ -O2 -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include \
 *                 -L/opt/homebrew/opt/libomp/lib -lomp 02_parallel_bubble_sort_merge_sort.cpp -o 02_parallel_bubble_sort_merge_sort
 * 
 *   Execution Command:
 *     ./02_parallel_bubble_sort_merge_sort
 * ======================================================================================
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <random>

#ifdef _OPENMP
#include <omp.h>
#endif

// ============================================================================
// 1. Sequential Bubble Sort
// ============================================================================
void sequentialBubbleSort(std::vector<int>& arr) {
    int n = static_cast<int>(arr.size());
    for (int i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

// ============================================================================
// 2. Parallel Bubble Sort (Odd-Even Transposition Sort using OpenMP)
// ============================================================================
void parallelBubbleSort(std::vector<int>& arr) {
    int n = static_cast<int>(arr.size());
    #pragma omp parallel
    {
        for (int phase = 0; phase < n; ++phase) {
            if (phase % 2 == 0) {
                // Even Phase: Compare and swap at even indices
                #pragma omp for schedule(static)
                for (int i = 0; i < n - 1; i += 2) {
                    if (arr[i] > arr[i + 1]) {
                        std::swap(arr[i], arr[i + 1]);
                    }
                }
            } else {
                // Odd Phase: Compare and swap at odd indices
                #pragma omp for schedule(static)
                for (int i = 1; i < n - 1; i += 2) {
                    if (arr[i] > arr[i + 1]) {
                        std::swap(arr[i], arr[i + 1]);
                    }
                }
            }
        }
    }
}

// ============================================================================
// 3. Sequential Merge Sort
// ============================================================================
void merge(std::vector<int>& arr, int left, int mid, int right, std::vector<int>& temp) {
    int i = left;
    int j = mid + 1;
    int k = left;

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }
    while (i <= mid) {
        temp[k++] = arr[i++];
    }
    while (j <= right) {
        temp[k++] = arr[j++];
    }
    for (int p = left; p <= right; ++p) {
        arr[p] = temp[p];
    }
}

void sequentialMergeSortHelper(std::vector<int>& arr, int left, int right, std::vector<int>& temp) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    sequentialMergeSortHelper(arr, left, mid, temp);
    sequentialMergeSortHelper(arr, mid + 1, right, temp);
    merge(arr, left, mid, right, temp);
}

void sequentialMergeSort(std::vector<int>& arr) {
    std::vector<int> temp(arr.size());
    sequentialMergeSortHelper(arr, 0, static_cast<int>(arr.size()) - 1, temp);
}

// ============================================================================
// 4. Parallel Merge Sort using OpenMP Tasks
// ============================================================================
const int MERGE_SORT_CUTOFF = 10000; // Switch to sequential below this threshold

void parallelMergeSortHelper(std::vector<int>& arr, int left, int right, std::vector<int>& temp) {
    if (left >= right) return;

    int mid = left + (right - left) / 2;

    if (right - left < MERGE_SORT_CUTOFF) {
        sequentialMergeSortHelper(arr, left, mid, temp);
        sequentialMergeSortHelper(arr, mid + 1, right, temp);
    } else {
        #pragma omp task shared(arr, temp)
        parallelMergeSortHelper(arr, left, mid, temp);

        #pragma omp task shared(arr, temp)
        parallelMergeSortHelper(arr, mid + 1, right, temp);

        #pragma omp taskwait
    }
    merge(arr, left, mid, right, temp);
}

void parallelMergeSort(std::vector<int>& arr) {
    std::vector<int> temp(arr.size());
    #pragma omp parallel
    {
        #pragma omp single
        {
            parallelMergeSortHelper(arr, 0, static_cast<int>(arr.size()) - 1, temp);
        }
    }
}

// ============================================================================
// Helper: Print Array
// ============================================================================
void printArray(const std::string& label, const std::vector<int>& arr, size_t limit = 10) {
    std::cout << "  " << std::left << std::setw(25) << label << ": [ ";
    size_t count = std::min(arr.size(), limit);
    for (size_t i = 0; i < count; ++i) {
        std::cout << arr[i] << (i + 1 < count ? ", " : "");
    }
    if (arr.size() > limit) {
        std::cout << ", ... (" << arr.size() << " items)";
    }
    std::cout << " ]\n";
}

// ============================================================================
// Main Function
// ============================================================================
int main() {
    std::cout << "================================================================================" << std::endl;
    std::cout << "  LP-5 High Performance Computing: Practical 2" << std::endl;
    std::cout << "  Parallel Bubble Sort and Merge Sort using OpenMP" << std::endl;
    std::cout << "================================================================================" << std::endl;

#ifdef _OPENMP
    std::cout << "  OpenMP Active: Using " << omp_get_max_threads() << " threads." << std::endl;
#else
    std::cout << "  OpenMP Not Enabled: Running in sequential mode." << std::endl;
#endif

    // ------------------------------------------------------------------------
    // Part A: Correctness Verification on Small Array (10 Elements)
    // ------------------------------------------------------------------------
    std::cout << "\n--------------------------------------------------------------------------------" << std::endl;
    std::cout << "  Part A: Verification on Small Array (10 Elements)" << std::endl;
    std::cout << "--------------------------------------------------------------------------------" << std::endl;

    std::vector<int> demoArray = {64, 34, 25, 12, 22, 11, 90, 88, 45, 50};
    printArray("Original Array", demoArray);

    auto bubbleCopySeq = demoArray;
    auto bubbleCopyPar = demoArray;
    auto mergeCopySeq = demoArray;
    auto mergeCopyPar = demoArray;

    sequentialBubbleSort(bubbleCopySeq);
    parallelBubbleSort(bubbleCopyPar);
    sequentialMergeSort(mergeCopySeq);
    parallelMergeSort(mergeCopyPar);

    printArray("Sequential Bubble Sort", bubbleCopySeq);
    printArray("Parallel Bubble Sort", bubbleCopyPar);
    printArray("Sequential Merge Sort", mergeCopySeq);
    printArray("Parallel Merge Sort", mergeCopyPar);

    // ------------------------------------------------------------------------
    // Part B: Performance Benchmark - Bubble Sort (N = 20,000)
    // ------------------------------------------------------------------------
    const int BUBBLE_N = 20000;
    std::cout << "\n--------------------------------------------------------------------------------" << std::endl;
    std::cout << "  Part B: Performance Benchmark - Bubble Sort (N = " << BUBBLE_N << ")" << std::endl;
    std::cout << "--------------------------------------------------------------------------------" << std::endl;

    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(1, 1000000);

    std::vector<int> bubbleDataSeq(BUBBLE_N);
    for (int i = 0; i < BUBBLE_N; ++i) {
        bubbleDataSeq[i] = dist(rng);
    }
    std::vector<int> bubbleDataPar = bubbleDataSeq;

    std::cout << "  Running Sequential Bubble Sort..." << std::flush;
    auto t1 = std::chrono::high_resolution_clock::now();
    sequentialBubbleSort(bubbleDataSeq);
    auto t2 = std::chrono::high_resolution_clock::now();
    double timeSeqBubble = std::chrono::duration<double, std::milli>(t2 - t1).count();
    std::cout << " Done (" << std::fixed << std::setprecision(2) << timeSeqBubble << " ms)" << std::endl;

    std::cout << "  Running Parallel Bubble Sort (Odd-Even)..." << std::flush;
    t1 = std::chrono::high_resolution_clock::now();
    parallelBubbleSort(bubbleDataPar);
    t2 = std::chrono::high_resolution_clock::now();
    double timeParBubble = std::chrono::duration<double, std::milli>(t2 - t1).count();
    std::cout << " Done (" << std::fixed << std::setprecision(2) << timeParBubble << " ms)" << std::endl;

    double speedupBubble = (timeParBubble > 0) ? (timeSeqBubble / timeParBubble) : 1.0;
    std::cout << "  Verification : " 
              << (std::is_sorted(bubbleDataPar.begin(), bubbleDataPar.end()) ? "PASSED (Sorted)" : "FAILED") << std::endl;
    std::cout << "  Speedup      : " << std::fixed << std::setprecision(2) << speedupBubble << "x" << std::endl;

    // ------------------------------------------------------------------------
    // Part C: Performance Benchmark - Merge Sort (N = 1,000,000)
    // ------------------------------------------------------------------------
    const int MERGE_N = 1000000;
    std::cout << "\n--------------------------------------------------------------------------------" << std::endl;
    std::cout << "  Part C: Performance Benchmark - Merge Sort (N = " << MERGE_N << ")" << std::endl;
    std::cout << "--------------------------------------------------------------------------------" << std::endl;

    std::vector<int> mergeDataSeq(MERGE_N);
    for (int i = 0; i < MERGE_N; ++i) {
        mergeDataSeq[i] = dist(rng);
    }
    std::vector<int> mergeDataPar = mergeDataSeq;

    std::cout << "  Running Sequential Merge Sort..." << std::flush;
    t1 = std::chrono::high_resolution_clock::now();
    sequentialMergeSort(mergeDataSeq);
    t2 = std::chrono::high_resolution_clock::now();
    double timeSeqMerge = std::chrono::duration<double, std::milli>(t2 - t1).count();
    std::cout << " Done (" << std::fixed << std::setprecision(2) << timeSeqMerge << " ms)" << std::endl;

    std::cout << "  Running Parallel Merge Sort (OpenMP Tasks)..." << std::flush;
    t1 = std::chrono::high_resolution_clock::now();
    parallelMergeSort(mergeDataPar);
    t2 = std::chrono::high_resolution_clock::now();
    double timeParMerge = std::chrono::duration<double, std::milli>(t2 - t1).count();
    std::cout << " Done (" << std::fixed << std::setprecision(2) << timeParMerge << " ms)" << std::endl;

    double speedupMerge = (timeParMerge > 0) ? (timeSeqMerge / timeParMerge) : 1.0;
    std::cout << "  Verification : " 
              << (std::is_sorted(mergeDataPar.begin(), mergeDataPar.end()) ? "PASSED (Sorted)" : "FAILED") << std::endl;
    std::cout << "  Speedup      : " << std::fixed << std::setprecision(2) << speedupMerge << "x" << std::endl;

    // ------------------------------------------------------------------------
    // Summary Comparison Table
    // ------------------------------------------------------------------------
    std::cout << "\n================================================================================" << std::endl;
    std::cout << "  PERFORMANCE COMPARISON SUMMARY" << std::endl;
    std::cout << "================================================================================" << std::endl;
    std::cout << "  " << std::left << std::setw(22) << "Algorithm"
              << std::setw(15) << "Input Size"
              << std::setw(18) << "Sequential (ms)"
              << std::setw(18) << "Parallel (ms)"
              << std::setw(12) << "Speedup" << std::endl;
    std::cout << "  " << std::string(80, '-') << std::endl;

    std::cout << "  " << std::left << std::setw(22) << "Bubble Sort (Odd-Even)"
              << std::setw(15) << BUBBLE_N
              << std::fixed << std::setprecision(2)
              << std::setw(18) << timeSeqBubble
              << std::setw(18) << timeParBubble
              << std::setw(12) << (std::to_string(speedupBubble).substr(0, 4) + "x") << std::endl;

    std::cout << "  " << std::left << std::setw(22) << "Merge Sort (Task-based)"
              << std::setw(15) << MERGE_N
              << std::fixed << std::setprecision(2)
              << std::setw(18) << timeSeqMerge
              << std::setw(18) << timeParMerge
              << std::setw(12) << (std::to_string(speedupMerge).substr(0, 4) + "x") << std::endl;
    std::cout << "================================================================================" << std::endl;

    return 0;
}

/**
 * ============================== SAMPLE OUTPUT ==============================
 * 
 * ================================================================================
 *   LP-5 High Performance Computing: Practical 2
 *   Parallel Bubble Sort and Merge Sort using OpenMP
 * ================================================================================
 *   OpenMP Active: Using 8 threads.
 * 
 * --------------------------------------------------------------------------------
 *   Part A: Verification on Small Array (10 Elements)
 * --------------------------------------------------------------------------------
 *   Original Array           : [ 64, 34, 25, 12, 22, 11, 90, 88, 45, 50 ]
 *   Sequential Bubble Sort   : [ 11, 12, 22, 25, 34, 45, 50, 64, 88, 90 ]
 *   Parallel Bubble Sort     : [ 11, 12, 22, 25, 34, 45, 50, 64, 88, 90 ]
 *   Sequential Merge Sort    : [ 11, 12, 22, 25, 34, 45, 50, 64, 88, 90 ]
 *   Parallel Merge Sort      : [ 11, 12, 22, 25, 34, 45, 50, 64, 88, 90 ]
 * 
 * --------------------------------------------------------------------------------
 *   Part B: Performance Benchmark - Bubble Sort (N = 20000)
 * --------------------------------------------------------------------------------
 *   Running Sequential Bubble Sort... Done (122.73 ms)
 *   Running Parallel Bubble Sort (Odd-Even)... Done (367.97 ms)
 *   Verification : PASSED (Sorted)
 *   Speedup      : 0.33x
 * 
 * --------------------------------------------------------------------------------
 *   Part C: Performance Benchmark - Merge Sort (N = 1000000)
 * --------------------------------------------------------------------------------
 *   Running Sequential Merge Sort... Done (46.80 ms)
 *   Running Parallel Merge Sort (OpenMP Tasks)... Done (18.94 ms)
 *   Verification : PASSED (Sorted)
 *   Speedup      : 2.47x
 * 
 * ================================================================================
 *   PERFORMANCE COMPARISON SUMMARY
 * ================================================================================
 *   Algorithm             Input Size     Sequential (ms)   Parallel (ms)     Speedup     
 *   --------------------------------------------------------------------------------
 *   Bubble Sort (Odd-Even)20000          122.73            367.97            0.33x       
 *   Merge Sort (Task-based)1000000        46.80             18.94             2.47x       
 * ================================================================================
 */
