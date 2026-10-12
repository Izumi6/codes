"""
================================================================================
  Program 4: 0-1 Knapsack Problem — Dynamic Programming & Branch and Bound
  Course: Design and Analysis of Algorithms (410241)

  Description:
    Given n items (each with a weight and value) and a knapsack of capacity W,
    select items to maximize value WITHOUT breaking items (0-1 constraint).

    Implements two strategies:
      1. Dynamic Programming (Bottom-Up Tabulation)
      2. Branch and Bound (Best-First Search using a max-heap)

  No external libraries required. Uses only Python standard library.
================================================================================
"""

import heapq


# ═══════════════════════════════════════════════════════════════════════════════
#  APPROACH 1: Dynamic Programming (Bottom-Up)
# ═══════════════════════════════════════════════════════════════════════════════

def knapsack_dp(weights, values, capacity, n):
    """
    Solve the 0-1 Knapsack problem using bottom-up dynamic programming.

    Time Complexity : O(n * W)
    Space Complexity: O(n * W)

    Returns:
        tuple: (max_value, selected_items)
    """
    # Build the DP table
    # dp[i][w] = maximum value achievable using items 0..i-1 with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Option 1: Exclude item i
            dp[i][w] = dp[i - 1][w]

            # Option 2: Include item i (if it fits)
            if weights[i - 1] <= w:
                include_value = dp[i - 1][w - weights[i - 1]] + values[i - 1]
                dp[i][w] = max(dp[i][w], include_value)

    # Backtrack to find which items were selected
    max_value = dp[n][capacity]
    selected_items = []
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i)  # item index (1-based)
            w -= weights[i - 1]

    selected_items.reverse()
    return max_value, selected_items


# ═══════════════════════════════════════════════════════════════════════════════
#  APPROACH 2: Branch and Bound (Best-First Search)
# ═══════════════════════════════════════════════════════════════════════════════

class BBNode:
    """Represents a node in the Branch and Bound search tree."""

    def __init__(self, level, value, weight, bound, selected):
        self.level = level        # depth in the decision tree (item index)
        self.value = value        # accumulated value so far
        self.weight = weight      # accumulated weight so far
        self.bound = bound        # upper bound on best achievable value
        self.selected = selected  # list of selected item indices

    def __lt__(self, other):
        # Max-heap: higher bound = higher priority (negate for heapq)
        return self.bound > other.bound


def compute_bound(node, n, capacity, weights, values):
    """
    Compute the upper bound for a B&B node using fractional relaxation.
    This is the key pruning mechanism — if the bound is less than the
    current best, we prune the subtree.
    """
    if node.weight >= capacity:
        return 0

    bound = node.value
    total_weight = node.weight
    j = node.level

    # Greedily add remaining items (fractionally if needed)
    while j < n and total_weight + weights[j] <= capacity:
        total_weight += weights[j]
        bound += values[j]
        j += 1

    # Add fractional part of the next item
    if j < n:
        bound += (capacity - total_weight) * (values[j] / weights[j])

    return bound


def knapsack_branch_and_bound(weights, values, capacity, n):
    """
    Solve the 0-1 Knapsack problem using Branch and Bound with best-first search.

    Time Complexity : O(2^n) worst case, but pruning makes it much faster.
    Space Complexity: O(2^n) worst case for the priority queue.

    Returns:
        tuple: (max_value, selected_items)
    """
    # Sort items by value/weight ratio (descending) for tighter bounds
    indices = list(range(n))
    indices.sort(key=lambda i: values[i] / weights[i], reverse=True)

    sorted_weights = [weights[i] for i in indices]
    sorted_values = [values[i] for i in indices]

    # Initialize root node
    root = BBNode(level=0, value=0, weight=0, bound=0, selected=[])
    root.bound = compute_bound(root, n, capacity, sorted_weights, sorted_values)

    max_value = 0
    best_selection = []
    priority_queue = [root]

    while priority_queue:
        current = heapq.heappop(priority_queue)

        # Pruning: skip if this node's bound can't beat current best
        if current.bound <= max_value:
            continue

        level = current.level
        if level >= n:
            continue

        # ── Branch 1: Include item at 'level' ────────────────────────────
        new_weight = current.weight + sorted_weights[level]
        new_value = current.value + sorted_values[level]

        if new_weight <= capacity:
            include_selected = current.selected + [indices[level]]

            if new_value > max_value:
                max_value = new_value
                best_selection = include_selected

            include_node = BBNode(
                level=level + 1,
                value=new_value,
                weight=new_weight,
                bound=0,
                selected=include_selected
            )
            include_node.bound = compute_bound(
                include_node, n, capacity, sorted_weights, sorted_values
            )

            if include_node.bound > max_value:
                heapq.heappush(priority_queue, include_node)

        # ── Branch 2: Exclude item at 'level' ────────────────────────────
        exclude_node = BBNode(
            level=level + 1,
            value=current.value,
            weight=current.weight,
            bound=0,
            selected=current.selected[:]
        )
        exclude_node.bound = compute_bound(
            exclude_node, n, capacity, sorted_weights, sorted_values
        )

        if exclude_node.bound > max_value:
            heapq.heappush(priority_queue, exclude_node)

    # Convert back to 1-based indices and sort
    best_selection = sorted([i + 1 for i in best_selection])
    return max_value, best_selection


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 65)
    print("   0-1 KNAPSACK — DYNAMIC PROGRAMMING & BRANCH AND BOUND")
    print("=" * 65)

    try:
        user_input = input("\n  Enter the number of items (press Enter for default 3 items): ").strip()
    except EOFError:
        user_input = ""
    if not user_input:
        print("  Using default sample items: Item 1 (w=10, v=60), Item 2 (w=20, v=100), Item 3 (w=30, v=120) with capacity=50")
        capacity = 50
        weights = [10, 20, 30]
        values = [60, 100, 120]
        n = 3
    else:
        n = int(user_input)
        capacity = int(input("  Enter the knapsack capacity: "))
        weights = []
        values = []
        print("\n  Enter item details:")
        print(f"  {'─' * 40}")

        for i in range(1, n + 1):
            w = int(input(f"    Item {i} — Weight : "))
            v = int(input(f"    Item {i} — Value  : "))
            weights.append(w)
            values.append(v)
            print()

    # ── Display Input ────────────────────────────────────────────────────
    print(f"\n  INPUT")
    print(f"  {'─' * 45}")
    print(f"  {'Item':<10} {'Weight':>10} {'Value':>10}")
    print(f"  {'─' * 45}")
    for i in range(n):
        print(f"  Item {i + 1:<5} {weights[i]:>10} {values[i]:>10}")
    print(f"  {'─' * 45}")
    print(f"  Knapsack Capacity: {capacity}")

    # ── Solve with Dynamic Programming ───────────────────────────────────
    dp_value, dp_items = knapsack_dp(weights, values, capacity, n)

    print(f"\n{'═' * 65}")
    print("  RESULT — Dynamic Programming (Bottom-Up)")
    print(f"{'═' * 65}")
    print(f"  Maximum Value    : {dp_value}")
    print(f"  Items Selected   : {', '.join(f'Item {i}' for i in dp_items)}")
    total_w = sum(weights[i - 1] for i in dp_items)
    print(f"  Total Weight Used: {total_w} / {capacity}")

    # ── Solve with Branch and Bound ──────────────────────────────────────
    bb_value, bb_items = knapsack_branch_and_bound(weights, values, capacity, n)

    print(f"\n{'═' * 65}")
    print("  RESULT — Branch and Bound (Best-First Search)")
    print(f"{'═' * 65}")
    print(f"  Maximum Value    : {bb_value}")
    print(f"  Items Selected   : {', '.join(f'Item {i}' for i in bb_items)}")
    total_w_bb = sum(weights[i - 1] for i in bb_items)
    print(f"  Total Weight Used: {total_w_bb} / {capacity}")

    # ── Verification ─────────────────────────────────────────────────────
    print(f"\n{'─' * 65}")
    if dp_value == bb_value:
        print("  ✓ Both methods agree on the optimal value.")
    else:
        print("  ✗ Results differ — please verify input.")
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Enter the number of items: 4
  Enter the knapsack capacity: 7
    Item 1 — Weight: 2, Value: 1
    Item 2 — Weight: 3, Value: 4
    Item 3 — Weight: 5, Value: 7
    Item 4 — Weight: 1, Value: 5

  RESULT — Dynamic Programming (Bottom-Up)
    Maximum Value    : 12
    Items Selected   : Item 3, Item 4
    Total Weight Used: 6 / 7

  RESULT — Branch and Bound (Best-First Search)
    Maximum Value    : 12
    Items Selected   : Item 3, Item 4
    Total Weight Used: 6 / 7

  ✓ Both methods agree on the optimal value.

========================================================================
"""
