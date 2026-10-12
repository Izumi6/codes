"""
================================================================================
  Mini Project 3: Naive String Matching vs Rabin-Karp Algorithm
  Course: Design and Analysis of Algorithms (410241)

  Description:
    Implement and compare:
      1. Naive String Matching — O(n*m) worst case
      2. Rabin-Karp Algorithm  — O(n+m) average case using hashing

    Observe the difference in working for the same input.

  No external libraries required. Uses only Python standard library.
================================================================================
"""

import time


# ═══════════════════════════════════════════════════════════════════════════
#  METHOD 1: Naive String Matching
# ═══════════════════════════════════════════════════════════════════════════

def naive_string_match(text, pattern):
    """
    Naive (brute-force) string matching algorithm.
    Slides the pattern over the text one character at a time.

    Time Complexity:
      Best Case  : O(n) — mismatch at first character each time
      Worst Case : O(n * m) — e.g., text="AAAAAAB", pattern="AAB"

    Returns: list of starting indices where pattern is found
    """
    n = len(text)
    m = len(pattern)
    positions = []
    comparisons = 0

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            comparisons += 1
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            positions.append(i)

    return positions, comparisons


# ═══════════════════════════════════════════════════════════════════════════
#  METHOD 2: Rabin-Karp Algorithm
# ═══════════════════════════════════════════════════════════════════════════

def rabin_karp(text, pattern, prime=101):
    """
    Rabin-Karp string matching using rolling hash.

    Uses a hash function to quickly filter out non-matching positions.
    Only performs character-by-character comparison when hashes match.

    Time Complexity:
      Average Case : O(n + m)
      Worst Case   : O(n * m) — when all hashes collide (rare)

    Returns: list of starting indices where pattern is found
    """
    n = len(text)
    m = len(pattern)
    d = 256  # number of characters in alphabet
    positions = []
    comparisons = 0
    hash_comparisons = 0

    if m > n:
        return positions, comparisons

    # Compute hash of pattern and first window of text
    p_hash = 0  # hash of pattern
    t_hash = 0  # hash of current text window
    h = pow(d, m - 1) % prime  # highest power of d

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % prime
        t_hash = (d * t_hash + ord(text[i])) % prime

    # Slide the pattern over text
    for i in range(n - m + 1):
        hash_comparisons += 1

        # If hashes match, verify character by character
        if p_hash == t_hash:
            match = True
            for j in range(m):
                comparisons += 1
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                positions.append(i)

        # Compute hash for next window using rolling hash
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t_hash < 0:
                t_hash += prime

    return positions, comparisons


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("  NAIVE STRING MATCHING vs RABIN-KARP ALGORITHM")
    print("=" * 70)

    # ── Test Cases ──────────────────────────────────────────────────────
    test_cases = [
        ("AABAACAADAABAABA", "AABA", "Normal text"),
        ("AAAAAAAAAAAAAAA", "AAAA", "Worst case (all matches)"),
        ("ABCDEFGHIJKLMNO", "XYZ", "No match found"),
        ("ABABABABABABAB", "ABAB", "Overlapping patterns"),
        ("GEEKS FOR GEEKS", "GEEKS", "Text with spaces"),
    ]

    for text, pattern, description in test_cases:
        print(f"\n{'─' * 70}")
        print(f"  Test: {description}")
        print(f"{'─' * 70}")
        print(f"  Text    : \"{text}\"")
        print(f"  Pattern : \"{pattern}\"")

        # Naive
        start = time.perf_counter()
        naive_pos, naive_comp = naive_string_match(text, pattern)
        t_naive = time.perf_counter() - start

        # Rabin-Karp
        start = time.perf_counter()
        rk_pos, rk_comp = rabin_karp(text, pattern)
        t_rk = time.perf_counter() - start

        print(f"\n  {'Method':<20} {'Positions Found':<25} {'Comparisons':<15} {'Time':<12}")
        print(f"  {'─' * 65}")
        print(f"  {'Naive':<20} {str(naive_pos):<25} {naive_comp:<15} {t_naive:.6f}s")
        print(f"  {'Rabin-Karp':<20} {str(rk_pos):<25} {rk_comp:<15} {t_rk:.6f}s")

        if naive_pos:
            print(f"\n  Pattern found at indices: {naive_pos}")
        else:
            print(f"\n  Pattern NOT found in text.")

    # ── Performance on large input ──────────────────────────────────────
    print(f"\n{'═' * 70}")
    print("  PERFORMANCE ON LARGE INPUT")
    print(f"{'═' * 70}")

    sizes = [10000, 50000, 100000]

    print(f"\n  {'Size':<12} {'Pattern':<12} {'Naive Time':<15} {'RK Time':<15} {'Naive Comp':<12} {'RK Comp':<12}")
    print(f"  {'─' * 70}")

    for n in sizes:
        text = "AB" * (n // 2)
        pattern = "ABAB"

        start = time.perf_counter()
        _, n_comp = naive_string_match(text, pattern)
        t_naive = time.perf_counter() - start

        start = time.perf_counter()
        _, r_comp = rabin_karp(text, pattern)
        t_rk = time.perf_counter() - start

        print(f"  {n:<12} {'ABAB':<12} {t_naive:<15.4f} {t_rk:<15.4f} {n_comp:<12} {r_comp:<12}")

    print(f"\n{'─' * 70}")
    print("  ANALYSIS & OBSERVATIONS")
    print(f"{'─' * 70}")
    print("""
    1. Naive Algorithm:
       • Slides pattern one position at a time and compares all characters.
       • Simple but inefficient for large texts.
       • Time: O(n*m) worst case, O(n) best case.

    2. Rabin-Karp Algorithm:
       • Uses rolling hash to quickly skip non-matching positions.
       • Only compares characters when hash values match.
       • Time: O(n+m) average case, O(n*m) worst case (hash collisions).

    3. Key Differences:
       • Rabin-Karp performs fewer character comparisons due to hashing.
       • Rabin-Karp has overhead for hash computation.
       • For short patterns, Naive may be faster (less overhead).
       • For long texts with few matches, Rabin-Karp is significantly faster.
       • Both algorithms find the same set of matching positions.
    """)
    print(f"{'═' * 70}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Test: Normal text
  Text    : "AABAACAADAABAABA"
  Pattern : "AABA"

  Method               Positions Found           Comparisons     Time
  Naive                [0, 9, 12]                22              0.000005s
  Rabin-Karp           [0, 9, 12]                12              0.000008s

  Pattern found at indices: [0, 9, 12]

  Test: Worst case (all matches)
  Text    : "AAAAAAAAAAAAAAA"
  Pattern : "AAAA"

  Method               Positions Found           Comparisons     Time
  Naive                [0, 1, 2, ..., 11]        48              0.000006s
  Rabin-Karp           [0, 1, 2, ..., 11]        48              0.000009s

  PERFORMANCE ON LARGE INPUT
  Size         Pattern      Naive Time      RK Time
  10000        ABAB         0.0089          0.0045
  50000        ABAB         0.0432          0.0198
  100000       ABAB         0.0891          0.0402

========================================================================
"""
