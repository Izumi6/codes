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


def print_board(board):
    """Display the chessboard simply using Q and dots."""
    for row in board:
        print("  " + " ".join("Q" if cell == 1 else "." for cell in row))


def main():
    print("--- 8-Queens Problem (Backtracking with First Queen Placed) ---")
    row = int(input("Enter row of first queen (1-8): ")) - 1
    col = int(input("Enter col of first queen (1-8): ")) - 1

    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        print("Error: Row and column must be between 1 and 8.")
        return

    # Initialize the board and place the first queen
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[row][col] = 1

    print(f"\nFirst queen placed at: Row {row + 1}, Col {col + 1}")

    # Solve using Backtracking
    solutions = []
    solve_queens(board, 0, solutions)

    if not solutions:
        print("No valid solution found with the first queen at this position.")
        return

    print(f"\nTotal solutions found: {len(solutions)}")
    print("\nSolution 1 Board:")
    print_board(solutions[0])

    print("\nQueen Positions (Row, Col):")
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if solutions[0][i][j] == 1:
                fixed = " (First Queen)" if (i == row and j == col) else ""
                print(f"  Row {i + 1}, Col {j + 1}{fixed}")


if __name__ == "__main__":
    main()

"""
SAMPLE OUTPUT:
----------------------------------------------
--- 8-Queens Problem (Backtracking with First Queen Placed) ---
Enter row of first queen (1-8): 1
Enter col of first queen (1-8): 1

First queen placed at: Row 1, Col 1

Total solutions found: 4

Solution 1 Board:
  Q . . . . . . .
  . . . . . . Q .
  . . . . Q . . .
  . . . . . . . Q
  . Q . . . . . .
  . . . Q . . . .
  . . . . . Q . .
  . . Q . . . . .

Queen Positions (Row, Col):
  Row 1, Col 1 (First Queen)
  Row 2, Col 7
  Row 3, Col 5
  Row 4, Col 8
  Row 5, Col 2
  Row 6, Col 4
  Row 7, Col 6
  Row 8, Col 3
----------------------------------------------
"""
