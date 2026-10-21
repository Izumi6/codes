"""
================================================================================
  Program 5: Binomial Coefficients using Dynamic Programming
  Course: Design and Analysis of Algorithms (410241)

  Description:
    Compute binomial coefficients C(n, k) — also written as "n choose k" —
    using dynamic programming based on Pascal's Triangle recurrence:

        C(n, k) = C(n-1, k-1) + C(n-1, k)

    Base cases:
        C(n, 0) = 1  (choosing nothing)
        C(n, n) = 1  (choosing everything)

  Time Complexity : O(n * k)
  Space Complexity: O(n * k) — stores the full Pascal's Triangle table.

  No external libraries required. Uses only Python standard library.
================================================================================
"""


def generate_binomial_table(n, k):
    """
    Build a 2D DP table of binomial coefficients C(i, j)
    for 0 ≤ i ≤ n and 0 ≤ j ≤ min(i, k).

    Parameters:
        n (int): Total number of elements.
        k (int): Number of elements to choose.

    Returns:
        list[list[int]]: The DP table where table[i][j] = C(i, j).
    """
    # Initialize table with zeros
    table = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            # Base cases: C(i, 0) = 1 and C(i, i) = 1
            if j == 0 or j == i:
                table[i][j] = 1
            else:
                # Pascal's Triangle recurrence
                table[i][j] = table[i - 1][j - 1] + table[i - 1][j]

    return table


def display_pascals_triangle(table, n, k):
    """
    Display Pascal's Triangle up to row n (limited to column k).
    """
    print(f"\n  PASCAL'S TRIANGLE (rows 0 to {n}, columns 0 to {k})")
    print(f"  {'─' * (8 * (k + 1) + 10)}")

    # Header row
    label = "n \\ k"
    header = f"  {label:<6}"
    for j in range(k + 1):
        header += f"{j:>8}"
    print(header)
    print(f"  {'─' * (8 * (k + 1) + 10)}")

    # Data rows
    for i in range(n + 1):
        row_str = f"  {i:<6}"
        for j in range(min(i, k) + 1):
            row_str += f"{table[i][j]:>8}"
        print(row_str)

    print(f"  {'─' * (8 * (k + 1) + 10)}")


def verify_with_formula(n, k):
    """
    Verify the DP result using the multiplicative formula:
        C(n, k) = n! / (k! * (n-k)!)
    Computed iteratively to avoid large intermediate factorials.
    """
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1

    # Optimize by using the smaller of k and n-k
    k = min(k, n - k)

    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)

    return result


def main():
    print("=" * 65)
    print("   BINOMIAL COEFFICIENTS — DYNAMIC PROGRAMMING")
    print("=" * 65)

    user_n = input("\n  Enter the value of n [Default: 5]: ").strip()
    n = int(user_n) if user_n else 5
    user_k = input(f"  Enter the value of k (k ≤ {n}) [Default: 2]: ").strip()
    k = int(user_k) if user_k else 2
    if not user_n and not user_k:
        print(f"  [Using default textbook sample: n = {n}, k = {k}]")

    if k > n:
        print("\n  [Error] k cannot be greater than n.")
        return
    if n < 0 or k < 0:
        print("\n  [Error] n and k must be non-negative integers.")
        return

    # ── Generate the DP Table ────────────────────────────────────────────
    table = generate_binomial_table(n, k)

    # ── Display Pascal's Triangle ────────────────────────────────────────
    display_pascals_triangle(table, n, k)

    # ── Display the Result ───────────────────────────────────────────────
    result_dp = table[n][k]
    result_formula = verify_with_formula(n, k)

    print(f"\n{'═' * 65}")
    print(f"  RESULT")
    print(f"{'═' * 65}")
    print(f"  C({n}, {k}) using DP Table      = {result_dp}")
    print(f"  C({n}, {k}) using Direct Formula = {result_formula}")
    print(f"{'─' * 65}")

    if result_dp == result_formula:
        print(f"  ✓ Both methods agree. C({n}, {k}) = {result_dp}")
    else:
        print(f"  ✗ Mismatch detected — please verify.")

    print(f"{'═' * 65}")

    # ── Additional: Display Some Useful Properties ───────────────────────
    print(f"\n  PROPERTIES OF C({n}, {k}):")
    print(f"  {'─' * 50}")
    print(f"  • Symmetry  : C({n}, {k}) = C({n}, {n - k}) = {table[n][min(n - k, k)] if n - k <= k else result_dp}")
    print(f"  • Row Sum   : Σ C({n}, j) for j=0..{n}  = 2^{n} = {2 ** n}")
    if n >= 1:
        print(f"  • Recurrence: C({n}, {k}) = C({n - 1}, {k - 1}) + C({n - 1}, {k})")
        left = table[n - 1][k - 1] if k - 1 >= 0 else 0
        right = table[n - 1][k] if k <= n - 1 else 0
        print(f"                          = {left} + {right} = {left + right}")
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Enter the value of n: 5
  Enter the value of k (k ≤ n): 2

  PASCAL'S TRIANGLE (rows 0 to 5, columns 0 to 2)
    n \ k      0       1       2
    0          1
    1          1       1
    2          1       2       1
    3          1       3       3
    4          1       4       6
    5          1       5      10

  RESULT
    C(5, 2) using DP Table      = 10
    C(5, 2) using Direct Formula = 10
    ✓ Both methods agree. C(5, 2) = 10

  PROPERTIES OF C(5, 2):
    Symmetry  : C(5, 2) = C(5, 3) = 10
    Row Sum   : Σ C(5, j) for j=0..5 = 2^5 = 32
    Recurrence: C(5, 2) = C(4, 1) + C(4, 2) = 4 + 6 = 10

========================================================================
"""
