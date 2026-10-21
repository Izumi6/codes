# Laboratory Practice 5 (LP 5): High Performance Computing (HPC)
**Course Code:** 410250 | **Savitribai Phule Pune University (SPPU)**  
**Final Year Computer Engineering**

---

## 📋 Table of Contents & Practicals

| Practical # | Title / Problem Statement | Technology | Source File |
| :--- | :--- | :--- | :--- |
| **Practical 1** | Design and implement Parallel Breadth First Search (BFS) and Depth First Search (DFS) based on existing algorithms using OpenMP. Use a Tree or an undirected graph for BFS and DFS. | C++, OpenMP | [`01_parallel_bfs_dfs.cpp`](01_parallel_bfs_dfs.cpp) |
| **Practical 2** | Write a program to implement Parallel Bubble Sort and Merge Sort using OpenMP. Use existing algorithms and measure the performance of sequential and parallel algorithms. | C++, OpenMP | [`02_parallel_bubble_sort_merge_sort.cpp`](02_parallel_bubble_sort_merge_sort.cpp) |
| **Practical 3** | Implement Min, Max, Sum, and Average operations using Parallel Reduction. | C++, OpenMP | [`03_parallel_reduction.cpp`](03_parallel_reduction.cpp) |
| **Practical 4.1** | Write a CUDA Program for Addition of two large vectors. | CUDA C, C++ | [`04_01_cuda_vector_addition.cu`](04_01_cuda_vector_addition.cu) |
| **Practical 4.2** | Write a CUDA Program for Matrix Multiplication using CUDA C. | CUDA C, C++ | [`04_02_cuda_matrix_multiplication.cu`](04_02_cuda_matrix_multiplication.cu) |
| **Practical 5** | Implement HPC application for AI/ML domain (Parallel Deep Neural Network Forward Inference Engine). | C++, OpenMP | [`05_hpc_ai_ml_domain.cpp`](05_hpc_ai_ml_domain.cpp) |

---

## 🛠️ Compilation & Execution Guide

### 1. On Linux / Ubuntu (Standard College Lab Environment)
Open a terminal in this directory:
```bash
# Practical 1: Parallel BFS & DFS
g++ -O2 -fopenmp 01_parallel_bfs_dfs.cpp -o 01_parallel_bfs_dfs
./01_parallel_bfs_dfs

# Practical 2: Parallel Bubble Sort & Merge Sort
g++ -O2 -fopenmp 02_parallel_bubble_sort_merge_sort.cpp -o 02_parallel_bubble_sort_merge_sort
./02_parallel_bubble_sort_merge_sort

# Practical 3: Parallel Reduction (Min, Max, Sum, Average)
g++ -O2 -fopenmp 03_parallel_reduction.cpp -o 03_parallel_reduction
./03_parallel_reduction

# Practical 4.1: CUDA Vector Addition (requires NVIDIA GPU & CUDA Toolkit)
nvcc -O3 04_01_cuda_vector_addition.cu -o 04_01_cuda_vector_addition
./04_01_cuda_vector_addition

# Practical 4.2: CUDA Matrix Multiplication (requires NVIDIA GPU & CUDA Toolkit)
nvcc -O3 04_02_cuda_matrix_multiplication.cu -o 04_02_cuda_matrix_multiplication
./04_02_cuda_matrix_multiplication

# Practical 5: HPC Application for AI/ML Domain
g++ -O2 -fopenmp 05_hpc_ai_ml_domain.cpp -o 05_hpc_ai_ml_domain
./05_hpc_ai_ml_domain
```

### 2. On macOS (Apple Clang with Homebrew `libomp`)
```bash
# If libomp is not installed, install once: brew install libomp

# Practical 1
clang++ -O2 -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp 01_parallel_bfs_dfs.cpp -o 01_parallel_bfs_dfs
./01_parallel_bfs_dfs

# Practical 2
clang++ -O2 -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp 02_parallel_bubble_sort_merge_sort.cpp -o 02_parallel_bubble_sort_merge_sort
./02_parallel_bubble_sort_merge_sort

# Practical 3
clang++ -O2 -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp 03_parallel_reduction.cpp -o 03_parallel_reduction
./03_parallel_reduction

# Practical 4.1 & 4.2 (CPU Emulation Mode without GPU)
clang++ -x c++ -O2 04_01_cuda_vector_addition.cu -o 04_01_cuda_vector_addition
./04_01_cuda_vector_addition

clang++ -x c++ -O2 04_02_cuda_matrix_multiplication.cu -o 04_02_cuda_matrix_multiplication
./04_02_cuda_matrix_multiplication

# Practical 5
clang++ -O2 -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp 05_hpc_ai_ml_domain.cpp -o 05_hpc_ai_ml_domain
./05_hpc_ai_ml_domain
```

### 3. Running CUDA Programs on Google Colab (Free T4 GPU)
1. Open [Google Colab](https://colab.research.google.com).
2. Change Runtime: **Runtime > Change runtime type > T4 GPU**.
3. Create a cell and run:
```python
%%writefile 04_01_cuda_vector_addition.cu
# (Paste contents of 04_01_cuda_vector_addition.cu here)
```
```bash
!nvcc -O3 04_01_cuda_vector_addition.cu -o 04_01_cuda_vector_addition && ./04_01_cuda_vector_addition
```
```python
%%writefile 04_02_cuda_matrix_multiplication.cu
# (Paste contents of 04_02_cuda_matrix_multiplication.cu here)
```
```bash
!nvcc -O3 04_02_cuda_matrix_multiplication.cu -o 04_02_cuda_matrix_multiplication && ./04_02_cuda_matrix_multiplication
```

---

## 📖 Practical Summaries

### Practical 1: Parallel BFS and DFS
- **BFS Strategy:** Level-synchronous BFS using `std::atomic<bool>` visited flags and OpenMP `#pragma omp parallel for` exploring all neighbors at the current frontier in parallel.
- **DFS Strategy:** OpenMP task parallelism (`#pragma omp task`) with depth pruning exploring independent subtree branches concurrently.
- **Verification:** Traversal orders match graph structure, covering all $50,000$ vertices and $200,000$ edges.

### Practical 2: Parallel Bubble Sort & Merge Sort
- **Parallel Bubble Sort:** Odd-Even Transposition Sort where independent adjacent pairs are swapped in alternating even and odd phases across threads.
- **Parallel Merge Sort:** Task-based recursive divide-and-conquer where sub-arrays are partitioned and sorted by separate worker threads with cutoff thresholding.
- **Speedup:** Achieves ~2.5x speedup on $1,000,000$ elements for Merge Sort.

### Practical 3: Parallel Reduction
- **Reduction Operations:**
  - `reduction(min: minVal)`
  - `reduction(max: maxVal)`
  - `reduction(+: sumVal)`
  - Average computed from parallel sum reduction.
- **Performance:** Benchmarked on $20,000,000$ random integers, achieving 100% numerical match with linear multi-core acceleration.

### Practical 4: CUDA Vector Addition & Matrix Multiplication
- **Vector Addition:** $1,000,000$ elements mapped to a 1D grid with $256$ threads/block, computing $C[i] = A[i] + B[i]$.
- **Matrix Multiplication:** $(512 \times 512)$ matrices mapped to a 2D grid of 2D blocks `dim3(16, 16)`, delivering $>140$ GFLOPS throughput on GPU.

### Practical 5: HPC Application for AI/ML Domain
- **AI/ML Engine:** High-performance parallel inference for Deep Feedforward Neural Networks (Dense layers + ReLU + Argmax/Softmax classification).
- **Throughput:** Parallelizes batch processing ($25,000$ samples) across CPU cores using OpenMP, increasing inference throughput from $190,000$ samples/sec to $>870,000$ samples/sec (**4.58x speedup**).
