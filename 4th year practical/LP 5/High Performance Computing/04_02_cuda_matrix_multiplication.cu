/*
 * ==============================================================================
 * LP-5 Practical 4.2: Matrix Multiplication using CUDA C
 * 
 * Problem Statement:
 *   Write a CUDA Program for:
 *   2. Matrix Multiplication using CUDA C
 * 
 * How to Compile & Run:
 *   - On Windows (with NVIDIA GPU & CUDA Toolkit installed):
 *       Open Command Prompt (cmd) or Developer Command Prompt:
 *       nvcc 04_02_cuda_matrix_multiplication.cu -o matrix_mul.exe
 *       matrix_mul.exe
 * 
 *   - On Linux / Ubuntu:
 *       nvcc 04_02_cuda_matrix_multiplication.cu -o matrix_mul
 *       ./matrix_mul
 * 
 *   - On Google Colab (Free T4 GPU runtime if lab PC does not have NVIDIA GPU):
 *       1. Select Runtime > Change runtime type > T4 GPU
 *       2. In a notebook cell run:
 *          !nvcc 04_02_cuda_matrix_multiplication.cu -o matrix_mul && ./matrix_mul
 * ==============================================================================
 */

#include <iostream>
#include <cuda_runtime.h>

using namespace std;

// -------------------------------------------------------------
// CUDA 2D Kernel for Matrix Multiplication: C = A * B
// Each thread computes one element: C[row][col]
// -------------------------------------------------------------
__global__ void matrixMul(int *a, int *b, int *c, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < n && col < n) {
        int sum = 0;
        for (int k = 0; k < n; k++) {
            sum += a[row * n + k] * b[k * n + col];
        }
        c[row * n + col] = sum;
    }
}

// Helper function to print a square matrix
void printMatrix(const string& name, int *matrix, int n) {
    cout << name << " (" << n << "x" << n << "):" << endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << matrix[i * n + j] << "\t";
        }
        cout << endl;
    }
    cout << endl;
}

int main() {
    cout << "=================================================" << endl;
    cout << "  LP-5 Practical 4.2: CUDA Matrix Multiplication" << endl;
    cout << "=================================================" << endl;

    int n = 4; // 4x4 Square Matrices (Easy to verify in viva)
    int size = n * n * sizeof(int);

    // 1. Allocate Host memory (CPU)
    int *h_a = new int[n * n];
    int *h_b = new int[n * n];
    int *h_c = new int[n * n];

    // Initialize sample values
    // Matrix A: values 1, 2, 3...
    // Matrix B: values 1, 1, 1...
    for (int i = 0; i < n * n; i++) {
        h_a[i] = i + 1;
        h_b[i] = (i % 2 == 0) ? 1 : 2;
    }

    // Print input matrices
    printMatrix("Matrix A", h_a, n);
    printMatrix("Matrix B", h_b, n);

    // 2. Allocate Device memory (GPU)
    int *d_a, *d_b, *d_c;
    cudaMalloc((void**)&d_a, size);
    cudaMalloc((void**)&d_b, size);
    cudaMalloc((void**)&d_c, size);

    // 3. Copy inputs from Host to Device
    cudaMemcpy(d_a, h_a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, size, cudaMemcpyHostToDevice);

    // 4. Kernel launch parameters (2D Grid and 2D Blocks)
    dim3 threadsPerBlock(2, 2); // 2x2 = 4 threads per block
    dim3 blocksPerGrid((n + threadsPerBlock.x - 1) / threadsPerBlock.x,
                       (n + threadsPerBlock.y - 1) / threadsPerBlock.y);

    cout << "Launching CUDA 2D Kernel..." << endl;
    matrixMul<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, n);

    // Wait for GPU to finish
    cudaDeviceSynchronize();

    // 5. Copy result from Device to Host
    cudaMemcpy(h_c, d_c, size, cudaMemcpyDeviceToHost);

    // 6. Display Result Matrix
    printMatrix("Result Matrix C (A * B)", h_c, n);

    cout << "Matrix Multiplication completed successfully on GPU!" << endl;
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
  LP-5 Practical 4.2: CUDA Matrix Multiplication
=================================================
Matrix A (4x4):
1	2	3	4	
5	6	7	8	
9	10	11	12	
13	14	15	16	

Matrix B (4x4):
1	2	1	2	
1	2	1	2	
1	2	1	2	
1	2	1	2	

Launching CUDA 2D Kernel...
Result Matrix C (A * B) (4x4):
10	20	10	20	
26	52	26	52	
42	84	42	84	
58	116	58	116	

Matrix Multiplication completed successfully on GPU!
=================================================
===========================================================================
*/
