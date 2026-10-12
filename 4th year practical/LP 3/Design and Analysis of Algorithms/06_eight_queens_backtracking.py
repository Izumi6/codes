"""
================================================================================
  Program 6: 8-Queens Problem using Backtracking
  Course: Design and Analysis of Algorithms (410241)

  Description:
    Place 8 queens on an 8×8 chessboard such that no two queens threaten
    each other (no two queens share the same row, column, or diagonal).

    The first queen's position is taken as input from the user.
    The remaining 7 queens are placed using backtracking.

  Time Complexity : O(n!) — worst case exploration of permutations.
  Space Complexity: O(n)  — recursion stack + board representation.

  No external libraries required. Uses only Python standard library.
================================================================================
"""

BOARD_SIZE = 8


def is_safe(board, row, col):
    """
    Check whether placing a queen at (row, col) is safe.
    We only need to check columns to the left since we place
    queens column by column (left to right).
    """
    # Check the same row (leftward)
    for j in range(col):
        if board[row][j] == 1:
            return False

    # Check upper-left diagonal
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Check lower-left diagonal
    i, j = row + 1, col - 1
    while i < BOARD_SIZE and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1

    return True


def solve_queens(board, col, solutions):
    """
    Recursively place queens column by column using backtracking.
    When all 8 columns are filled, a valid solution is recorded.
    """
    if col >= BOARD_SIZE:
        # All queens placed successfully — record the solution
        solution = [row[:] for row in board]
        solutions.append(solution)
        return

    # If a queen is already placed in this column (the first queen),
    # skip to the next column
    for r in range(BOARD_SIZE):
        if board[r][col] == 1:
            solve_queens(board, col + 1, solutions)
            return

    # Try placing a queen in each row of this column
    for row in range(BOARD_SIZE):
        if is_safe(board, row, col):
            board[row][col] = 1           # place queen
            solve_queens(board, col + 1, solutions)
            board[row][col] = 0           # backtrack


def print_board(board, solution_num=None):
    """Display the chessboard in a visually clear format."""
    if solution_num is not None:
        print(f"\n  ── Solution {solution_num} {'─' * 40}")

    print(f"\n       {'   '.join(str(c + 1) for c in range(BOARD_SIZE))}")
    print(f"     ┌{'───┬' * (BOARD_SIZE - 1)}───┐")

    for i in range(BOARD_SIZE):
        row_str = f"  {i + 1}  │"
        for j in range(BOARD_SIZE):
            if board[i][j] == 1:
                row_str += " Q │"
            else:
                row_str += " · │"
        print(row_str)

        if i < BOARD_SIZE - 1:
            print(f"     ├{'───┼' * (BOARD_SIZE - 1)}───┤")

    print(f"     └{'───┴' * (BOARD_SIZE - 1)}───┘")


def main():
    print("=" * 60)
    print("   8-QUEENS PROBLEM — BACKTRACKING")
    print("=" * 60)

    print("\n  Place the first Queen on the board (press Enter for default Row 1, Col 1).")
    try:
        input_row = input("  Enter row    (1-8, default 1): ").strip()
    except EOFError:
        input_row = ""
    row = (int(input_row) - 1) if input_row else 0

    try:
        input_col = input("  Enter column (1-8, default 1): ").strip()
    except EOFError:
        input_col = ""
    col = (int(input_col) - 1) if input_col else 0

    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        print("\n  [Error] Row and column must be between 1 and 8.")
        return

    # Initialize the board and place the first queen
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[row][col] = 1

    print(f"\n  First Queen placed at ({row + 1}, {col + 1})")
    print_board(board)

    # ── Solve using Backtracking ─────────────────────────────────────────
    solutions = []
    solve_queens(board, 0, solutions)

    # ── Display Results ──────────────────────────────────────────────────
    if not solutions:
        print(f"\n{'═' * 60}")
        print("  No valid solution exists with the first Queen at "
              f"({row + 1}, {col + 1}).")
        print(f"{'═' * 60}\n")
        return

    print(f"\n{'═' * 60}")
    print(f"  TOTAL SOLUTIONS FOUND: {len(solutions)}")
    print(f"{'═' * 60}")

    # Show the first solution in detail
    print_board(solutions[0], solution_num=1)

    # Show queen positions for the first solution
    print(f"\n  Queen Positions (Solution 1):")
    print(f"  {'─' * 30}")
    queen_num = 1
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if solutions[0][i][j] == 1:
                marker = " ← First Queen" if (i == row and j == col) else ""
                print(f"    Queen {queen_num}: Row {i + 1}, Col {j + 1}{marker}")
                queen_num += 1

    # If more solutions exist, show a summary
    if len(solutions) > 1:
        print(f"\n  Showing up to 3 more solutions:")
        for idx in range(1, min(4, len(solutions))):
            print_board(solutions[idx], solution_num=idx + 1)

    print(f"\n{'═' * 60}")
    print(f"  Total valid configurations with Q1 at "
          f"({row + 1}, {col + 1}): {len(solutions)}")
    print(f"{'═' * 60}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Enter row (1-8): 1
  Enter column (1-8): 1

  First Queen placed at (1, 1)

  TOTAL SOLUTIONS FOUND: 4

  Queen Positions (Solution 1):
    Queen 1: Row 1, Col 1  ← First Queen
    Queen 2: Row 2, Col 7
    Queen 3: Row 3, Col 5
    Queen 4: Row 4, Col 8
    Queen 5: Row 5, Col 2
    Queen 6: Row 6, Col 4
    Queen 7: Row 7, Col 6
    Queen 8: Row 8, Col 3

  Total valid configurations with Q1 at (1, 1): 4

========================================================================
"""
