"""
================================================================================
  Program 3: Fractional Knapsack Problem — Greedy Method
  Course: Design and Analysis of Algorithms (410241)

  Description:
    Given n items, each with a weight and a value, and a knapsack of
    capacity W, determine the maximum value obtainable by filling the
    knapsack. Items may be broken into fractions (hence "fractional").

  Greedy Strategy:
    1. Compute the value-to-weight ratio for each item.
    2. Sort items by this ratio in descending order.
    3. Greedily pick items (fully or fractionally) until the knapsack is full.

  Time Complexity : O(n log n) — dominated by sorting.
  Space Complexity: O(n)

  No external libraries required. Uses only Python standard library.
================================================================================
"""


class Item:
    """Represents an item with a weight, value, and computed ratio."""

    def __init__(self, item_id, weight, value):
        self.item_id = item_id
        self.weight = weight
        self.value = value
        self.ratio = value / weight  # value per unit weight

    def __repr__(self):
        return f"Item({self.item_id}, w={self.weight}, v={self.value})"


def fractional_knapsack(items, capacity):
    """
    Solve the Fractional Knapsack problem using the greedy approach.

    Parameters:
        items    (list[Item]): List of available items.
        capacity (float):      Maximum weight the knapsack can hold.

    Returns:
        tuple: (max_value, selections)
            - max_value:  Total value obtained.
            - selections: List of (Item, fraction_taken) tuples.
    """
    # Sort by value-to-weight ratio in descending order
    items_sorted = sorted(items, key=lambda x: x.ratio, reverse=True)

    remaining_capacity = capacity
    max_value = 0.0
    selections = []

    for item in items_sorted:
        if remaining_capacity <= 0:
            break

        if item.weight <= remaining_capacity:
            # Take the entire item
            fraction = 1.0
            remaining_capacity -= item.weight
            max_value += item.value
        else:
            # Take only the fraction that fits
            fraction = remaining_capacity / item.weight
            max_value += item.value * fraction
            remaining_capacity = 0

        selections.append((item, fraction))

    return max_value, selections


def main():
    print("=" * 65)
    print("   FRACTIONAL KNAPSACK PROBLEM — GREEDY METHOD")
    print("=" * 65)

    user_input = input("\n  Enter the number of items [Press Enter for default sample (3 items)]: ").strip()
    if not user_input:
        print("  [Using default textbook sample: Capacity = 50, 3 items]")
        capacity = 50.0
        items = [
            Item(item_id=1, weight=10.0, value=60.0),
            Item(item_id=2, weight=20.0, value=100.0),
            Item(item_id=3, weight=30.0, value=120.0)
        ]
    else:
        n = int(user_input)
        capacity = float(input("  Enter the knapsack capacity: "))
        items = []
        print("\n  Enter item details (weight and value for each):")
        print(f"  {'─' * 40}")

        for i in range(1, n + 1):
            weight = float(input(f"    Item {i} — Weight : "))
            value = float(input(f"    Item {i} — Value  : "))
            items.append(Item(item_id=i, weight=weight, value=value))
            print()

    # ── Display Input ────────────────────────────────────────────────────
    print(f"\n  INPUT ITEMS (sorted by Value/Weight ratio)")
    print(f"  {'─' * 58}")
    print(f"  {'Item':<8} {'Weight':>8} {'Value':>8} {'Ratio (V/W)':>14}")
    print(f"  {'─' * 58}")

    for item in sorted(items, key=lambda x: x.ratio, reverse=True):
        print(f"  Item {item.item_id:<3} {item.weight:>8.2f} {item.value:>8.2f} {item.ratio:>14.4f}")
    print(f"  {'─' * 58}")
    print(f"  Knapsack Capacity: {capacity:.2f}")

    # ── Solve ────────────────────────────────────────────────────────────
    max_value, selections = fractional_knapsack(items, capacity)

    # ── Display Results ──────────────────────────────────────────────────
    print(f"\n{'═' * 65}")
    print("  OPTIMAL SELECTION")
    print(f"{'═' * 65}")
    print(f"  {'Item':<8} {'Weight':>8} {'Value':>8} {'Fraction':>10} {'Contribution':>14}")
    print(f"  {'─' * 58}")

    total_weight = 0.0
    for item, fraction in selections:
        weight_taken = item.weight * fraction
        value_taken = item.value * fraction
        total_weight += weight_taken
        frac_display = f"{fraction * 100:.1f}%"
        print(f"  Item {item.item_id:<3} {item.weight:>8.2f} {item.value:>8.2f} "
              f"{frac_display:>10} {value_taken:>14.2f}")

    print(f"  {'─' * 58}")
    print(f"  {'Total Weight Used:':<36} {total_weight:>14.2f}")
    print(f"  {'Maximum Value Obtained:':<36} {max_value:>14.2f}")
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Enter the number of items: 3
  Enter the knapsack capacity: 50
    Item 1 — Weight: 10, Value: 60
    Item 2 — Weight: 20, Value: 100
    Item 3 — Weight: 30, Value: 120

  INPUT ITEMS (sorted by Value/Weight ratio)
    Item     Weight    Value    Ratio (V/W)
    Item 1    10.00    60.00       6.0000
    Item 2    20.00   100.00       5.0000
    Item 3    30.00   120.00       4.0000

  OPTIMAL SELECTION
    Item 1    100.0%    Contribution:  60.00
    Item 2    100.0%    Contribution: 100.00
    Item 3     66.7%    Contribution:  80.00
    Total Weight Used:      50.00
    Maximum Value Obtained: 240.00

========================================================================
"""
