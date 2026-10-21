# High Performance Computing - Mini Projects

SPPU BE Computer Engineering (2019 Pattern)

This directory contains simple, clean, and workable implementations of all HPC mini projects designed for practical demonstrations, viva examinations, and performance evaluations.

---

## Mini Projects Overview

| No. | Project Title | Parallel Paradigm / Hardware | Source File | Key Metric / Result |
|:---:|:---|:---|:---|:---|
| **6** | **Parallel Quicksort Algorithm** | Distributed Memory (MPI) / Task Parallelism | [06_parallel_quicksort_mpi.cpp](06_parallel_quicksort_mpi.cpp) | Speedup: ~2.35x across 4 processes |
| **7** | **Huffman Encoding on GPU** | NVIDIA CUDA C++ / Parallel Reduction | [07_huffman_encoding_gpu.cu](07_huffman_encoding_gpu.cu) | Compression: 1.96x (48.92% space saving) |
| **8** | **Parallel Database Query Optimization** | Shared Memory (OpenMP) / Parallel Hash Join | [08_parallel_database_query_optimization.cpp](08_parallel_database_query_optimization.cpp) | 500,000 records filtered, joined & aggregated |
| **9** | **Non-Serial Polyadic DP on GPU** | CUDA C++ / Anti-Diagonal Wavefront Kernel | [09_non_serial_polyadic_dp_gpu.cu](09_non_serial_polyadic_dp_gpu.cu) | Concurrent anti-diagonal matrix chain DP |

---

## Compilation & Execution Guide

### 6. Parallel Quicksort using MPI
```bash
# With MPI installed (OpenMPI / MS-MPI):
mpic++ -O2 06_parallel_quicksort_mpi.cpp -o quicksort_mpi
mpirun -np 4 ./quicksort_mpi

# Standalone execution (standard C++17):
g++ -std=c++17 -O2 06_parallel_quicksort_mpi.cpp -o quicksort_mpi
./quicksort_mpi
```

### 7. Huffman Encoding on GPU
```bash
# On NVIDIA GPU Systems (with CUDA Toolkit):
nvcc -O2 07_huffman_encoding_gpu.cu -o huffman_gpu
./huffman_gpu

# On CPU / Mac systems (portable wrapper):
g++ -std=c++17 -O2 07_huffman_encoding_gpu.cu -o huffman_gpu
./huffman_gpu
```

### 8. Parallel Database Query Optimization
```bash
# With OpenMP:
g++ -std=c++17 -O2 -fopenmp 08_parallel_database_query_optimization.cpp -o db_opt
./db_opt

# macOS Clang:
clang++ -std=c++17 -O2 08_parallel_database_query_optimization.cpp -o db_opt
./db_opt
```

### 9. Non-Serial Polyadic DP on GPU
```bash
# On NVIDIA GPU Systems:
nvcc -O2 09_non_serial_polyadic_dp_gpu.cu -o nsp_dp_gpu
./nsp_dp_gpu

# On CPU / Mac systems:
g++ -std=c++17 -O2 09_non_serial_polyadic_dp_gpu.cu -o nsp_dp_gpu
./nsp_dp_gpu
```

---

## Detailed Project Descriptions & Viva Questions

### 6. Parallel Quicksort using MPI
- **Problem Statement**: Evaluate performance enhancement of parallel Quicksort Algorithm using MPI.
- **Approach**: Domain decomposition partitions the dataset among MPI ranks. Each rank independently executes sequential quicksort, followed by tree-reduction merge across ranks.
- **Viva Q&A**:
  - *Q: Why use MPI instead of OpenMP for Quicksort?*
    *A: MPI allows distributed memory scaling across multiple network nodes and clusters, bypassing single-machine RAM limits.*
  - *Q: What is Speedup and Efficiency?*
    *A: Speedup $S = T_{\text{seq}} / T_{\text{par}}$. Efficiency $E = S / P$ (where $P$ is the number of processing cores).*

### 7. Huffman Encoding on GPU
- **Problem Statement**: Implement Huffman Encoding on GPU.
- **Approach**: Character frequency counting uses an atomic histogram kernel on GPU. The priority queue constructs the binary prefix tree on host, and GPU threads encode characters in parallel.
- **Viva Q&A**:
  - *Q: How does GPU accelerate Huffman Encoding?*
    *A: Character frequency histogram generation and data stream substitution are embarrassing parallel operations computed concurrently across thousands of GPU cores.*

### 8. Parallel Database Query Optimization
- **Problem Statement**: Implement Parallelization of Database Query optimization.
- **Approach**: Benchmarks a realistic analytical SQL query (`SELECT ... JOIN ... WHERE ... GROUP BY ...`) on 500,000 order records using parallel table filtering, parallel hash join, and thread-local accumulator reduction.
- **Viva Q&A**:
  - *Q: How does parallel hash join improve query performance?*
    *A: It builds a hash table on the smaller dimension table and parallelizes the probe phase across CPU cores using OpenMP.*

### 9. Non-Serial Polyadic Dynamic Programming with GPU
- **Problem Statement**: Implement Non-Serial Polyadic Dynamic Programming with GPU Parallelization.
- **Approach**: Parallelizes Matrix Chain Multiplication using the anti-diagonal (wavefront) technique. Cells on the same anti-diagonal $L$ are mutually independent and computed concurrently by GPU threads.
- **Viva Q&A**:
  - *Q: What does Non-Serial Polyadic mean in DP?*
    *A: 'Polyadic' means the recurrence involves multiple subproblems on the right-hand side. 'Non-serial' means dependencies span a 2D table requiring diagonal-by-diagonal pipeline computation.*
