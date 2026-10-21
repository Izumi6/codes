/*
 * ==============================================================================
 * LP-5 Practical 3: Min, Max, Sum, and Average using Parallel Reduction
 * 
 * Problem Statement:
 *   Implement Min, Max, Sum and Average operations using Parallel Reduction.
 * 
 * How to Compile & Run:
 *   - On Windows (MinGW GCC):
 *       g++ -fopenmp 03_parallel_reduction.cpp -o 03_parallel_reduction.exe
 *       03_parallel_reduction.exe
 * 
 *   - On Linux / Ubuntu:
 *       g++ -fopenmp 03_parallel_reduction.cpp -o 03_parallel_reduction
 *       ./03_parallel_reduction
 * ==============================================================================
 */

#include <iostream>
#include <vector>
#include <cstdlib>
#include <iomanip>
#include <omp.h>

using namespace std;

// -------------------------------------------------------------
// Parallel Reduction Operations
// -------------------------------------------------------------
int parallelMin(const vector<int>& arr) {
    int min_val = arr[0];
    int n = arr.size();

    #pragma omp parallel for reduction(min: min_val)
    for (int i = 0; i < n; i++) {
        if (arr[i] < min_val) {
            min_val = arr[i];
        }
    }
    return min_val;
}

int parallelMax(const vector<int>& arr) {
    int max_val = arr[0];
    int n = arr.size();

    #pragma omp parallel for reduction(max: max_val)
    for (int i = 0; i < n; i++) {
        if (arr[i] > max_val) {
            max_val = arr[i];
        }
    }
    return max_val;
}

long long parallelSum(const vector<int>& arr) {
    long long sum = 0;
    int n = arr.size();

    #pragma omp parallel for reduction(+: sum)
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}

double parallelAverage(const vector<int>& arr) {
    long long sum = parallelSum(arr);
    return (double)sum / arr.size();
}

int main() {
    cout << "=================================================" << endl;
    cout << "  LP-5 Practical 3: Parallel Reduction" << endl;
    cout << "=================================================" << endl;

    // Part 1: Small Array Demonstration
    vector<int> smallArr = {15, 8, 42, 4, 23, 16, 99, 1, 55, 30};
    cout << "Sample Array: ";
    for (int val : smallArr) cout << val << " ";
    cout << endl;

    cout << "\nResults on Sample Array:" << endl;
    cout << "  Minimum Value : " << parallelMin(smallArr) << endl;
    cout << "  Maximum Value : " << parallelMax(smallArr) << endl;
    cout << "  Sum of Values : " << parallelSum(smallArr) << endl;
    cout << "  Average Value : " << fixed << setprecision(2) << parallelAverage(smallArr) << endl;

    // Part 2: Large Array Performance Benchmark (N = 1,000,000)
    int N = 1000000;
    cout << "\n--- Performance on Large Array (N = " << N << ") ---" << endl;
    vector<int> largeArr(N);
    for (int i = 0; i < N; i++) {
        largeArr[i] = rand() % 1000 + 1; // Random numbers between 1 and 1000
    }

    double start = omp_get_wtime();
    int minVal = parallelMin(largeArr);
    int maxVal = parallelMax(largeArr);
    long long sumVal = parallelSum(largeArr);
    double avgVal = (double)sumVal / N;
    double end = omp_get_wtime();

    cout << "  Parallel Min : " << minVal << endl;
    cout << "  Parallel Max : " << maxVal << endl;
    cout << "  Parallel Sum : " << sumVal << endl;
    cout << "  Parallel Avg : " << fixed << setprecision(2) << avgVal << endl;
    cout << "  Total Execution Time: " << fixed << setprecision(4) << (end - start) << " seconds" << endl;

    cout << "=================================================" << endl;
    return 0;
}

/*
============================== SAMPLE OUTPUT ==============================
=================================================
  LP-5 Practical 3: Parallel Reduction
=================================================
Sample Array: 15 8 42 4 23 16 99 1 55 30 

Results on Sample Array:
  Minimum Value : 1
  Maximum Value : 99
  Sum of Values : 293
  Average Value : 29.30

--- Performance on Large Array (N = 1000000) ---
  Parallel Min : 1
  Parallel Max : 1000
  Parallel Sum : 500388612
  Parallel Avg : 500.39
  Total Execution Time: 0.0035 seconds
=================================================
===========================================================================
*/
