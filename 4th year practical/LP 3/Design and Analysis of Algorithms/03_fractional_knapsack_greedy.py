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
    print("--- Fractional Knapsack Problem (Greedy Method) ---")
    n = int(input("Enter number of items: "))
    capacity = float(input("Enter knapsack capacity: "))
    items = []
    for i in range(1, n + 1):
        weight = float(input(f"Item {i} Weight: "))
        value = float(input(f"Item {i} Value : "))
        items.append(Item(item_id=i, weight=weight, value=value))

    print(f"\nKnapsack Capacity: {capacity:.2f}")
    print("\nItems sorted by Value/Weight ratio:")
    for item in sorted(items, key=lambda x: x.ratio, reverse=True):
        print(f"  Item {item.item_id}: Weight = {item.weight:.1f}, Value = {item.value:.1f}, Ratio = {item.ratio:.2f}")

    max_value, selections = fractional_knapsack(items, capacity)

    print("\nSelected Items:")
    total_weight = 0.0
    for item, fraction in selections:
        weight_taken = item.weight * fraction
        value_taken = item.value * fraction
        total_weight += weight_taken
        print(f"  Item {item.item_id}: Taken = {fraction * 100:.1f}%, Weight = {weight_taken:.1f}, Value = {value_taken:.1f}")

    print(f"\nTotal Weight Used  : {total_weight:.2f}")
    print(f"Maximum Total Value: {max_value:.2f}")


if __name__ == "__main__":
    main()

"""
SAMPLE OUTPUT:
----------------------------------------------
--- Fractional Knapsack Problem (Greedy Method) ---
Enter number of items: 3
Enter knapsack capacity: 50
Item 1 Weight: 10
Item 1 Value : 60
Item 2 Weight: 20
Item 2 Value : 100
Item 3 Weight: 30
Item 3 Value : 120

Knapsack Capacity: 50.00

Items sorted by Value/Weight ratio:
  Item 1: Weight = 10.0, Value = 60.0, Ratio = 6.00
  Item 2: Weight = 20.0, Value = 100.0, Ratio = 5.00
  Item 3: Weight = 30.0, Value = 120.0, Ratio = 4.00

Selected Items:
  Item 1: Taken = 100.0%, Weight = 10.0, Value = 60.0
  Item 2: Taken = 100.0%, Weight = 20.0, Value = 100.0
  Item 3: Taken = 66.7%, Weight = 20.0, Value = 80.0

Total Weight Used  : 50.00
Maximum Total Value: 240.00
----------------------------------------------
"""
