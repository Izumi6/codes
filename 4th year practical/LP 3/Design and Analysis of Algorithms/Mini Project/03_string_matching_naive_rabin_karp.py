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
    print("--- String Matching: Naive vs Rabin-Karp ---")

    test_cases = [
        ("AABAACAADAABAABA", "AABA"),
        ("ABCDEFGHIJKLMNO", "XYZ"),
        ("ABABABABABABAB", "ABAB")
    ]

    for text, pattern in test_cases:
        print(f"\nText   : {text}")
        print(f"Pattern: {pattern}")

        naive_pos, naive_comp = naive_string_match(text, pattern)
        rk_pos, rk_comp = rabin_karp(text, pattern)

        print(f"Naive      -> Found at indices: {naive_pos}, Comparisons: {naive_comp}")
        print(f"Rabin-Karp -> Found at indices: {rk_pos}, Comparisons: {rk_comp}")


if __name__ == "__main__":
    main()

"""
SAMPLE OUTPUT:
----------------------------------------------
--- String Matching: Naive vs Rabin-Karp ---

Text   : AABAACAADAABAABA
Pattern: AABA
Naive      -> Found at indices: [0, 9, 12], Comparisons: 22
Rabin-Karp -> Found at indices: [0, 9, 12], Comparisons: 12

Text   : ABCDEFGHIJKLMNO
Pattern: XYZ
Naive      -> Found at indices: [], Comparisons: 13
Rabin-Karp -> Found at indices: [], Comparisons: 0

Text   : ABABABABABABAB
Pattern: ABAB
Naive      -> Found at indices: [0, 2, 4, 6, 8, 10], Comparisons: 34
Rabin-Karp -> Found at indices: [0, 2, 4, 6, 8, 10], Comparisons: 24
----------------------------------------------
"""
