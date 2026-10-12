"""
================================================================================
  Mini Project 1: Matrix Multiplication — Single-threaded vs Multithreaded
  Course: Design and Analysis of Algorithms (410241)

  Description:
    Implement matrix multiplication using:
      1. Standard (single-threaded) approach
      2. Multithreaded — one thread per row
      3. Multithreaded — one thread per cell
    Compare performance of all three approaches.

  No external libraries required. Uses only Python standard library.
  Requirements: None (uses built-in threading module)
================================================================================
"""

import threading
import time
import random


def generate_matrix(rows, cols):
    """Generate a random matrix of given dimensions."""
    return [[random.randint(1, 10) for _ in range(cols)] for _ in range(rows)]


def print_matrix(matrix, name="Matrix"):
    """Print a matrix in formatted form (only for small matrices)."""
    print(f"\n  {name}:")
    for row in matrix:
        print(f"    {row}")


# ═══════════════════════════════════════════════════════════════════════════
#  METHOD 1: Standard Matrix Multiplication (Single-threaded)
# ═══════════════════════════════════════════════════════════════════════════

def standard_multiply(A, B):
    """Standard O(n³) matrix multiplication."""
    rows_A, cols_A = len(A), len(A[0])
    cols_B = len(B[0])
    result = [[0] * cols_B for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result


# ═══════════════════════════════════════════════════════════════════════════
#  METHOD 2: Multithreaded — One Thread Per Row
# ═══════════════════════════════════════════════════════════════════════════

def multiply_row(A, B, result, row):
    """Compute one row of the result matrix."""
    cols_B = len(B[0])
    cols_A = len(A[0])
    for j in range(cols_B):
        for k in range(cols_A):
            result[row][j] += A[row][k] * B[k][j]


def threaded_multiply_per_row(A, B):
    """Matrix multiplication with one thread per row."""
    rows_A = len(A)
    cols_B = len(B[0])
    result = [[0] * cols_B for _ in range(rows_A)]

    threads = []
    for i in range(rows_A):
        t = threading.Thread(target=multiply_row, args=(A, B, result, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return result


# ═══════════════════════════════════════════════════════════════════════════
#  METHOD 3: Multithreaded — One Thread Per Cell
# ═══════════════════════════════════════════════════════════════════════════

def multiply_cell(A, B, result, row, col):
    """Compute one cell of the result matrix."""
    cols_A = len(A[0])
    for k in range(cols_A):
        result[row][col] += A[row][k] * B[k][col]


def threaded_multiply_per_cell(A, B):
    """Matrix multiplication with one thread per cell."""
    rows_A = len(A)
    cols_B = len(B[0])
    result = [[0] * cols_B for _ in range(rows_A)]

    threads = []
    for i in range(rows_A):
        for j in range(cols_B):
            t = threading.Thread(target=multiply_cell, args=(A, B, result, i, j))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    return result


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("  MATRIX MULTIPLICATION — SINGLE-THREADED vs MULTITHREADED")
    print("=" * 70)

    # Small matrix demo
    print(f"\n{'─' * 70}")
    print("  DEMO: 3×3 Matrix Multiplication")
    print(f"{'─' * 70}")

    A_small = generate_matrix(3, 3)
    B_small = generate_matrix(3, 3)
    print_matrix(A_small, "Matrix A")
    print_matrix(B_small, "Matrix B")

    result = standard_multiply(A_small, B_small)
    print_matrix(result, "Result (A × B)")

    # Performance comparison with larger matrices
    sizes = [50, 100, 150]

    print(f"\n{'═' * 70}")
    print("  PERFORMANCE COMPARISON")
    print(f"{'═' * 70}")
    print(f"\n  {'Size':<10} {'Standard':<18} {'Thread/Row':<18} {'Thread/Cell':<18}")
    print(f"  {'─' * 62}")

    for n in sizes:
        A = generate_matrix(n, n)
        B = generate_matrix(n, n)

        # Standard
        start = time.perf_counter()
        standard_multiply(A, B)
        t_std = time.perf_counter() - start

        # Thread per row
        start = time.perf_counter()
        threaded_multiply_per_row(A, B)
        t_row = time.perf_counter() - start

        # Thread per cell (only for smaller sizes due to thread overhead)
        if n <= 100:
            start = time.perf_counter()
            threaded_multiply_per_cell(A, B)
            t_cell = time.perf_counter() - start
            cell_str = f"{t_cell:.4f}s"
        else:
            cell_str = "Skipped (too many threads)"

        print(f"  {n}×{n:<7} {t_std:.4f}s{'':<10} {t_row:.4f}s{'':<10} {cell_str}")

    print(f"\n{'─' * 70}")
    print("  ANALYSIS")
    print(f"{'─' * 70}")
    print("""
    1. Standard method is straightforward with O(n³) complexity.
    2. Thread-per-row creates n threads — moderate overhead.
    3. Thread-per-cell creates n² threads — high overhead for large matrices.
    4. Due to Python's GIL (Global Interpreter Lock), multithreading
       may NOT provide speedup for CPU-bound tasks in Python.
    5. In languages like C/Java, thread-per-row shows significant speedup.
    6. Thread-per-cell has excessive overhead and is usually slower.
    """)
    print(f"{'═' * 70}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  DEMO: 3×3 Matrix Multiplication
  Matrix A:
    [3, 7, 2]
    [5, 1, 8]
    [4, 6, 9]
  Matrix B:
    [1, 4, 6]
    [8, 2, 3]
    [5, 7, 1]
  Result (A × B):
    [69, 40, 41]
    [53, 78, 41]
    [97, 91, 51]

  PERFORMANCE COMPARISON
  Size       Standard           Thread/Row         Thread/Cell
  50×50      0.0125s            0.0134s            0.0892s
  100×100    0.0982s            0.0745s            0.9124s
  150×150    0.3214s            0.2485s            Skipped

  ANALYSIS
    Standard is straightforward with O(n³) complexity.
    Thread-per-row creates n threads — moderate overhead.
    Thread-per-cell creates n² threads — excessive overhead.

========================================================================
"""
