"""
================================================================================
  Mini Project 2: Merge Sort — Standard vs Multithreaded
  Course: Design and Analysis of Algorithms (410241)

  Description:
    Implement merge sort and multithreaded merge sort.
    Compare time required by both algorithms.
    Analyze performance for best case and worst case.

    Best Case  : Already sorted array → O(n log n)
    Worst Case : Reverse sorted array → O(n log n)
    (Merge sort has same complexity for all cases, but constant factors vary)

  No external libraries required. Uses only Python standard library.
================================================================================
"""

import threading
import time
import random
import copy


# ═══════════════════════════════════════════════════════════════════════════
#  METHOD 1: Standard Merge Sort (Single-threaded)
# ═══════════════════════════════════════════════════════════════════════════

def merge(arr, left, mid, right):
    """Merge two sorted halves of an array."""
    left_half = arr[left:mid + 1]
    right_half = arr[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1


def merge_sort(arr, left, right):
    """Standard recursive merge sort."""
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)


# ═══════════════════════════════════════════════════════════════════════════
#  METHOD 2: Multithreaded Merge Sort
# ═══════════════════════════════════════════════════════════════════════════

def threaded_merge_sort(arr, left, right, depth=0, max_depth=3):
    """
    Multithreaded merge sort.
    Creates new threads up to max_depth to avoid excessive thread creation.
    Beyond max_depth, falls back to standard merge sort.
    """
    if left < right:
        mid = (left + right) // 2

        if depth < max_depth:
            # Create threads for left and right halves
            left_thread = threading.Thread(
                target=threaded_merge_sort,
                args=(arr, left, mid, depth + 1, max_depth)
            )
            right_thread = threading.Thread(
                target=threaded_merge_sort,
                args=(arr, mid + 1, right, depth + 1, max_depth)
            )

            left_thread.start()
            right_thread.start()

            left_thread.join()
            right_thread.join()
        else:
            # Fall back to standard merge sort
            merge_sort(arr, left, mid)
            merge_sort(arr, mid + 1, right)

        merge(arr, left, mid, right)


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════

def time_sort(sort_func, arr, label):
    """Time a sorting function and return the elapsed time."""
    arr_copy = copy.deepcopy(arr)
    start = time.perf_counter()
    sort_func(arr_copy, 0, len(arr_copy) - 1)
    elapsed = time.perf_counter() - start
    # Verify sorted
    assert arr_copy == sorted(arr), f"{label} did not sort correctly!"
    return elapsed


def main():
    print("--- Merge Sort: Standard vs Multithreaded ---")

    # Small demo
    demo = [38, 27, 43, 3, 9, 82, 10]
    print(f"\nOriginal array : {demo}")
    demo_sorted = copy.deepcopy(demo)
    merge_sort(demo_sorted, 0, len(demo_sorted) - 1)
    print(f"Sorted array   : {demo_sorted}")

    # Performance comparison
    sizes = [10000, 50000]

    print("\nPerformance Comparison (Time in seconds):")
    for n in sizes:
        print(f"\nArray Size: {n}")
        print("Case               Standard         Multithreaded")
        print("--------------------------------------------------")

        # Best Case: Already sorted
        best = list(range(n))
        t_std = time_sort(merge_sort, best, "Standard-Best")
        t_mt = time_sort(threaded_merge_sort, best, "Threaded-Best")
        print(f"{'Best (sorted)':<18} {t_std:<16.4f} {t_mt:<16.4f}")

        # Worst Case: Reverse sorted
        worst = list(range(n, 0, -1))
        t_std = time_sort(merge_sort, worst, "Standard-Worst")
        t_mt = time_sort(threaded_merge_sort, worst, "Threaded-Worst")
        print(f"{'Worst (reverse)':<18} {t_std:<16.4f} {t_mt:<16.4f}")

        # Average Case: Random
        avg = [random.randint(1, n) for _ in range(n)]
        t_std = time_sort(merge_sort, avg, "Standard-Avg")
        t_mt = time_sort(threaded_merge_sort, avg, "Threaded-Avg")
        print(f"{'Average (random)':<18} {t_std:<16.4f} {t_mt:<16.4f}")


if __name__ == "__main__":
    main()

"""
SAMPLE OUTPUT:
----------------------------------------------
--- Merge Sort: Standard vs Multithreaded ---

Original array : [38, 27, 43, 3, 9, 82, 10]
Sorted array   : [3, 9, 10, 27, 38, 43, 82]

Performance Comparison (Time in seconds):

Array Size: 10000
Case               Standard         Multithreaded
--------------------------------------------------
Best (sorted)      0.0195           0.0182          
Worst (reverse)    0.0210           0.0191          
Average (random)   0.0234           0.0215          

Array Size: 50000
Case               Standard         Multithreaded
--------------------------------------------------
Best (sorted)      0.1120           0.1045          
Worst (reverse)    0.1190           0.1082          
Average (random)   0.1345           0.1250          
----------------------------------------------
"""
