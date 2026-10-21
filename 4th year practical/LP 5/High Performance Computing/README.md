# LP 5: High Performance Computing (HPC)
**Course:** Laboratory Practice 5 (410250) | **SPPU Final Year Computer Engineering**

---

## 📋 Practicals List

| Practical | File Name | Description |
|:---|:---|:---|
| **1** | [`01_parallel_bfs_dfs.cpp`](01_parallel_bfs_dfs.cpp) | Parallel Breadth First Search (BFS) and Depth First Search (DFS) using OpenMP |
| **2** | [`02_parallel_bubble_sort_merge_sort.cpp`](02_parallel_bubble_sort_merge_sort.cpp) | Parallel Bubble Sort (Odd-Even) and Merge Sort using OpenMP |
| **3** | [`03_parallel_reduction.cpp`](03_parallel_reduction.cpp) | Min, Max, Sum, and Average operations using Parallel Reduction |
| **4.1** | [`04_01_cuda_vector_addition.cu`](04_01_cuda_vector_addition.cu) | CUDA program for addition of two large vectors |
| **4.2** | [`04_02_cuda_matrix_multiplication.cu`](04_02_cuda_matrix_multiplication.cu) | CUDA program for matrix multiplication |
| **5** | [`05_hpc_ai_ml_domain.cpp`](05_hpc_ai_ml_domain.cpp) | HPC application for AI/ML (Parallel Neural Network Layer Forward Pass) |

---

## 💻 How to Compile and Run (Windows Lab PC)

### 1. OpenMP C++ Programs (Practicals 1, 2, 3, 5)
In Windows Command Prompt (`cmd`) or MinGW terminal:

```cmd
:: Practical 1: Parallel BFS and DFS
g++ -fopenmp 01_parallel_bfs_dfs.cpp -o 01_parallel_bfs_dfs.exe
01_parallel_bfs_dfs.exe

:: Practical 2: Parallel Bubble Sort & Merge Sort
g++ -fopenmp 02_parallel_bubble_sort_merge_sort.cpp -o 02_parallel_bubble_sort_merge_sort.exe
02_parallel_bubble_sort_merge_sort.exe

:: Practical 3: Parallel Reduction (Min, Max, Sum, Avg)
g++ -fopenmp 03_parallel_reduction.cpp -o 03_parallel_reduction.exe
03_parallel_reduction.exe

:: Practical 5: HPC in AI/ML (Neural Network Layer)
g++ -fopenmp 05_hpc_ai_ml_domain.cpp -o 05_hpc_ai_ml_domain.exe
05_hpc_ai_ml_domain.exe
```

---

### 2. CUDA Programs (Practical 4.1 & 4.2)

#### Option A: On Windows PC with NVIDIA GPU & CUDA Toolkit
Open Developer Command Prompt for Visual Studio / cmd:
```cmd
:: Practical 4.1: Vector Addition
nvcc 04_01_cuda_vector_addition.cu -o vector_add.exe
vector_add.exe

:: Practical 4.2: Matrix Multiplication
nvcc 04_02_cuda_matrix_multiplication.cu -o matrix_mul.exe
matrix_mul.exe
```

#### Option B: On Google Colab (If Lab PC doesn't have an NVIDIA GPU)
1. Open Google Colab and set Runtime to **T4 GPU** (`Runtime > Change runtime type > T4 GPU`).
2. Run in a cell:
```bash
!nvcc 04_01_cuda_vector_addition.cu -o vector_add && ./vector_add
!nvcc 04_02_cuda_matrix_multiplication.cu -o matrix_mul && ./matrix_mul
```

---

## 🐧 Running on Linux / Ubuntu
```bash
g++ -fopenmp 01_parallel_bfs_dfs.cpp -o 01_parallel_bfs_dfs && ./01_parallel_bfs_dfs
g++ -fopenmp 02_parallel_bubble_sort_merge_sort.cpp -o 02_parallel_bubble_sort_merge_sort && ./02_parallel_bubble_sort_merge_sort
g++ -fopenmp 03_parallel_reduction.cpp -o 03_parallel_reduction && ./03_parallel_reduction
nvcc 04_01_cuda_vector_addition.cu -o vector_add && ./vector_add
nvcc 04_02_cuda_matrix_multiplication.cu -o matrix_mul && ./matrix_mul
g++ -fopenmp 05_hpc_ai_ml_domain.cpp -o 05_hpc_ai_ml_domain && ./05_hpc_ai_ml_domain
```
