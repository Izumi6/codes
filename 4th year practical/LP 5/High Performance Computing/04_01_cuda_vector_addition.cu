/*
 * ==============================================================================
 * LP-5 Practical 4.1: Vector Addition using CUDA C
 * 
 * Problem Statement:
 *   Write a CUDA Program for:
 *   1. Addition of two large vectors
 * 
 * How to Compile & Run:
 *   - On Windows (with NVIDIA GPU & CUDA Toolkit installed):
 *       Open Command Prompt (cmd) or Developer Command Prompt:
 *       nvcc 04_01_cuda_vector_addition.cu -o vector_add.exe
 *       vector_add.exe
 * 
 *   - On Linux / Ubuntu:
 *       nvcc 04_01_cuda_vector_addition.cu -o vector_add
 *       ./vector_add
 * 
 *   - On Google Colab (Free T4 GPU runtime if lab PC does not have NVIDIA GPU):
 *       1. Select Runtime > Change runtime type > T4 GPU
 *       2. In a notebook cell run:
 *          !nvcc 04_01_cuda_vector_addition.cu -o vector_add && ./vector_add
 * ==============================================================================
 */

#include <iostream>
#include <cuda_runtime.h>

using namespace std;

// -------------------------------------------------------------
// CUDA Kernel for Vector Addition
// Each thread computes one element: c[id] = a[id] + b[id]
// -------------------------------------------------------------
__global__ void vectorAdd(int *a, int *b, int *c, int n) {
    int id = blockDim.x * blockIdx.x + threadIdx.x;
    if (id < n) {
        c[id] = a[id] + b[id];
    }
}

int main() {
    cout << "=================================================" << endl;
    cout << "  LP-5 Practical 4.1: CUDA Vector Addition" << endl;
    cout << "=================================================" << endl;

    int n = 10000; // Vector size (10,000 elements)
    int size = n * sizeof(int);

    // 1. Allocate Host memory (CPU)
    int *h_a = new int[n];
    int *h_b = new int[n];
    int *h_c = new int[n];

    // Initialize input vectors
    for (int i = 0; i < n; i++) {
        h_a[i] = i + 1;        // 1, 2, 3, 4, ...
        h_b[i] = (i + 1) * 2;  // 2, 4, 6, 8, ...
    }

    // 2. Allocate Device memory (GPU)
    int *d_a, *d_b, *d_c;
    cudaMalloc((void**)&d_a, size);
    cudaMalloc((void**)&d_b, size);
    cudaMalloc((void**)&d_c, size);

    // 3. Copy inputs from Host (CPU) to Device (GPU)
    cudaMemcpy(d_a, h_a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, size, cudaMemcpyHostToDevice);

    // 4. Kernel launch parameters
    int threadsPerBlock = 256;
    int blocksPerGrid = (n + threadsPerBlock - 1) / threadsPerBlock;

    cout << "Vector Size       : " << n << " elements" << endl;
    cout << "Threads per Block : " << threadsPerBlock << endl;
    cout << "Blocks in Grid    : " << blocksPerGrid << endl;
    cout << "\nLaunching CUDA Kernel..." << endl;

    // Launch CUDA Kernel on GPU
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, n);

    // Wait for GPU to finish
    cudaDeviceSynchronize();

    // 5. Copy result back from Device (GPU) to Host (CPU)
    cudaMemcpy(h_c, d_c, size, cudaMemcpyDeviceToHost);

    // 6. Display first 10 results to verify correctness
    cout << "\nResults (First 10 elements):" << endl;
    cout << "Index\tA\t+\tB\t=\tC" << endl;
    cout << "-----------------------------------------" << endl;
    for (int i = 0; i < 10; i++) {
        cout << i << "\t" << h_a[i] << "\t+\t" << h_b[i] << "\t=\t" << h_c[i] << endl;
    }

    // Display last element
    cout << "...\n" << (n - 1) << "\t" << h_a[n - 1] << "\t+\t" << h_b[n - 1] << "\t=\t" << h_c[n - 1] << endl;

    cout << "\nVector Addition completed successfully on GPU!" << endl;
    cout << "=================================================" << endl;

    // 7. Free allocated memory
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    delete[] h_a;
    delete[] h_b;
    delete[] h_c;

    return 0;
}

/*
============================== SAMPLE OUTPUT ==============================
=================================================
  LP-5 Practical 4.1: CUDA Vector Addition
=================================================
Vector Size       : 10000 elements
Threads per Block : 256
Blocks in Grid    : 40

Launching CUDA Kernel...

Results (First 10 elements):
Index	A	+	B	=	C
-----------------------------------------
0	1	+	2	=	3
1	2	+	4	=	6
2	3	+	6	=	9
3	4	+	8	=	12
4	5	+	10	=	15
5	6	+	12	=	18
6	7	+	14	=	21
7	8	+	16	=	24
8	9	+	18	=	27
9	10	+	20	=	30
...
9999	10000	+	20000	=	30000

Vector Addition completed successfully on GPU!
=================================================
===========================================================================
*/
