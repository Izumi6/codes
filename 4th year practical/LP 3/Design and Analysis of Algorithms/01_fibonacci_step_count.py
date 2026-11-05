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


def main():
    print("--- Fibonacci Number Calculation (Recursive vs Non-Recursive) ---")
    n = int(input("Enter n: "))

    if n < 0:
        print("Error: n must be a non-negative integer.")
        return

    print(f"\nCalculating Fibonacci for n = {n}...\n")

    # 1. Recursive
    if n <= 30:
        step_counter_rec = {'count': 0}
        start = time.perf_counter()
        result_rec = fibonacci_recursive(n, step_counter_rec)
        elapsed_rec = time.perf_counter() - start

        print("1. Naive Recursive Approach:")
        print(f"   Fibonacci({n}) = {result_rec}")
        print(f"   Step Count     = {step_counter_rec['count']}")
        print(f"   Time Taken     = {elapsed_rec:.6f} seconds\n")
    else:
        print("1. Naive Recursive Approach: Skipped (n > 30 is too slow)\n")

    # 2. Iterative
    start = time.perf_counter()
    result_iter, steps_iter = fibonacci_iterative(n)
    elapsed_iter = time.perf_counter() - start

    print("2. Iterative (Non-Recursive) Approach:")
    print(f"   Fibonacci({n}) = {result_iter}")
    print(f"   Step Count     = {steps_iter}")
    print(f"   Time Taken     = {elapsed_iter:.6f} seconds\n")

    # 3. Memoized
    step_counter_memo = {'count': 0}
    memo = {}
    start = time.perf_counter()
    result_memo = fibonacci_memoized(n, memo, step_counter_memo)
    elapsed_memo = time.perf_counter() - start

    print("3. Dynamic Programming (Memoized) Approach:")
    print(f"   Fibonacci({n}) = {result_memo}")
    print(f"   Step Count     = {step_counter_memo['count']}")
    print(f"   Time Taken     = {elapsed_memo:.6f} seconds\n")

    # Summary
    print("Summary:")
    print("Method           Steps        Time (s)")
    print("---------------------------------------")
    if n <= 30:
        print(f"Recursive        {step_counter_rec['count']:<12} {elapsed_rec:.6f}")
    print(f"Iterative        {steps_iter:<12} {elapsed_iter:.6f}")
    print(f"Memoized (DP)    {step_counter_memo['count']:<12} {elapsed_memo:.6f}")


if __name__ == "__main__":
    main()

"""
SAMPLE OUTPUT:
----------------------------------------------
--- Fibonacci Number Calculation (Recursive vs Non-Recursive) ---
Enter n: 10

Calculating Fibonacci for n = 10...

1. Naive Recursive Approach:
   Fibonacci(10) = 55
   Step Count     = 177
   Time Taken     = 0.000021 seconds

2. Iterative (Non-Recursive) Approach:
   Fibonacci(10) = 55
   Step Count     = 9
   Time Taken     = 0.000001 seconds

3. Dynamic Programming (Memoized) Approach:
   Fibonacci(10) = 55
   Step Count     = 19
   Time Taken     = 0.000004 seconds

Summary:
Method           Steps        Time (s)
---------------------------------------
Recursive        177          0.000021
Iterative        9            0.000001
Memoized (DP)    19           0.000004
----------------------------------------------
"""
