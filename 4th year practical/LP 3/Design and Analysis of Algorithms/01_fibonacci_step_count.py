"""
================================================================================
  Program 1: Fibonacci Number Calculation with Step Count Analysis
  Course: Design and Analysis of Algorithms (410241)
  
  Description:
    Computes Fibonacci numbers using three approaches:
      1. Recursive (with step counting)
      2. Iterative (with step counting)
      3. Dynamic Programming - Memoization (with step counting)
    Compares the step counts across methods to demonstrate algorithmic efficiency.

  No external libraries required. Uses only Python standard library.
================================================================================
"""

import time


def fibonacci_recursive(n, step_counter):
    """
    Compute the n-th Fibonacci number using naive recursion.
    Time Complexity : O(2^n)
    Space Complexity: O(n) — due to call stack depth
    """
    step_counter['count'] += 1  # count each function call as a step

    if n <= 0:
        return 0
    if n == 1:
        return 1

    return fibonacci_recursive(n - 1, step_counter) + fibonacci_recursive(n - 2, step_counter)


def fibonacci_iterative(n):
    """
    Compute the n-th Fibonacci number using bottom-up iteration.
    Time Complexity : O(n)
    Space Complexity: O(1)
    """
    step_count = 0

    if n <= 0:
        step_count += 1
        return 0, step_count
    if n == 1:
        step_count += 1
        return 1, step_count

    prev, curr = 0, 1
    for i in range(2, n + 1):
        prev, curr = curr, prev + curr
        step_count += 1  # each addition is counted as a step

    return curr, step_count


def fibonacci_memoized(n, memo, step_counter):
    """
    Compute the n-th Fibonacci number using top-down memoization.
    Time Complexity : O(n)
    Space Complexity: O(n)
    """
    step_counter['count'] += 1

    if n in memo:
        return memo[n]

    if n <= 0:
        memo[n] = 0
    elif n == 1:
        memo[n] = 1
    else:
        memo[n] = (fibonacci_memoized(n - 1, memo, step_counter)
                    + fibonacci_memoized(n - 2, memo, step_counter))

    return memo[n]


def display_separator(char='─', width=70):
    print(char * width)


def main():
    print("=" * 70)
    print("   FIBONACCI NUMBER CALCULATION WITH STEP COUNT ANALYSIS")
    print("=" * 70)

    user_input = input("\n  Enter the value of n (recommended ≤ 30 for recursive) [Default: 10]: ").strip()
    n = int(user_input) if user_input else 10
    if not user_input:
        print(f"  [Using default: n = {n}]")

    if n < 0:
        print("  [Error] n must be a non-negative integer.")
        return

    # ── Method 1: Recursive ──────────────────────────────────────────────
    print(f"\n{'─' * 70}")
    print("  METHOD 1: Naive Recursive Approach")
    print(f"{'─' * 70}")

    if n <= 30:
        step_counter_rec = {'count': 0}
        start = time.perf_counter()
        result_rec = fibonacci_recursive(n, step_counter_rec)
        elapsed_rec = time.perf_counter() - start

        print(f"  Fibonacci({n})  = {result_rec}")
        print(f"  Step Count     = {step_counter_rec['count']}")
        print(f"  Time Elapsed   = {elapsed_rec:.6f} seconds")
    else:
        print("  [Skipped] n > 30 — recursive approach is too slow.")

    # ── Method 2: Iterative ──────────────────────────────────────────────
    print(f"\n{'─' * 70}")
    print("  METHOD 2: Iterative (Bottom-Up) Approach")
    print(f"{'─' * 70}")

    start = time.perf_counter()
    result_iter, steps_iter = fibonacci_iterative(n)
    elapsed_iter = time.perf_counter() - start

    print(f"  Fibonacci({n})  = {result_iter}")
    print(f"  Step Count     = {steps_iter}")
    print(f"  Time Elapsed   = {elapsed_iter:.6f} seconds")

    # ── Method 3: Memoized ───────────────────────────────────────────────
    print(f"\n{'─' * 70}")
    print("  METHOD 3: Memoized (Top-Down DP) Approach")
    print(f"{'─' * 70}")

    step_counter_memo = {'count': 0}
    memo = {}
    start = time.perf_counter()
    result_memo = fibonacci_memoized(n, memo, step_counter_memo)
    elapsed_memo = time.perf_counter() - start

    print(f"  Fibonacci({n})  = {result_memo}")
    print(f"  Step Count     = {step_counter_memo['count']}")
    print(f"  Time Elapsed   = {elapsed_memo:.6f} seconds")

    # ── Comparison Table ─────────────────────────────────────────────────
    print(f"\n{'═' * 70}")
    print("  STEP COUNT COMPARISON")
    print(f"{'═' * 70}")
    print(f"  {'Method':<25} {'Steps':>12} {'Time (sec)':>15}")
    print(f"  {'─' * 25} {'─' * 12} {'─' * 15}")

    if n <= 30:
        print(f"  {'Recursive':<25} {step_counter_rec['count']:>12,} {elapsed_rec:>15.6f}")
    else:
        print(f"  {'Recursive':<25} {'N/A':>12} {'N/A':>15}")

    print(f"  {'Iterative':<25} {steps_iter:>12,} {elapsed_iter:>15.6f}")
    print(f"  {'Memoized (DP)':<25} {step_counter_memo['count']:>12,} {elapsed_memo:>15.6f}")
    print(f"{'═' * 70}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Enter the value of n (recommended ≤ 30 for recursive): 10

  METHOD 1: Naive Recursive Approach
    Fibonacci(10)  = 55
    Step Count     = 177
    Time Elapsed   = 0.000021 seconds

  METHOD 2: Iterative (Bottom-Up) Approach
    Fibonacci(10)  = 55
    Step Count     = 9
    Time Elapsed   = 0.000001 seconds

  METHOD 3: Memoized (Top-Down DP) Approach
    Fibonacci(10)  = 55
    Step Count     = 19
    Time Elapsed   = 0.000004 seconds

  STEP COUNT COMPARISON
    Method                          Steps      Time (sec)
    Recursive                         177        0.000021
    Iterative                           9        0.000001
    Memoized (DP)                      19        0.000004

========================================================================
"""
