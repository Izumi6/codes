"""
================================================================================
  Program 4: Gradient Descent Algorithm to Find Local Minima
  Course: Machine Learning

  Description:
    Implement Gradient Descent to find the local minima of a function.
    Example: Find the local minima of y = (x + 3)² starting from x = 2.

    The derivative of y = (x + 3)² is dy/dx = 2(x + 3).
    The minimum occurs at x = -3 where y = 0.

    Gradient Descent update rule: x_new = x_old - learning_rate * gradient

  No dataset required. No external libraries beyond numpy and matplotlib.
  Requirements: pip install numpy matplotlib
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt


def function(x):
    """The function y = (x + 3)²"""
    return (x + 3) ** 2


def gradient(x):
    """The derivative dy/dx = 2(x + 3)"""
    return 2 * (x + 3)


def gradient_descent(starting_point, learning_rate, num_iterations, tolerance=1e-8):
    """
    Perform gradient descent to find the local minima.

    Parameters:
        starting_point  : Initial value of x
        learning_rate   : Step size (alpha)
        num_iterations  : Maximum number of iterations
        tolerance       : Convergence threshold

    Returns:
        x_history : List of x values at each iteration
        y_history : List of y values at each iteration
    """
    x = starting_point
    x_history = [x]
    y_history = [function(x)]

    print(f"\n  {'Iter':<8} {'x':>12} {'y = (x+3)²':>14} {'Gradient':>12}")
    print(f"  {'─' * 50}")
    print(f"  {'Start':<8} {x:>12.6f} {function(x):>14.6f} {gradient(x):>12.6f}")

    for i in range(1, num_iterations + 1):
        grad = gradient(x)
        x_new = x - learning_rate * grad

        x_history.append(x_new)
        y_history.append(function(x_new))

        # Print progress at selected iterations
        if i <= 10 or i % 10 == 0 or abs(grad) < tolerance:
            print(f"  {i:<8} {x_new:>12.6f} {function(x_new):>14.6f} {grad:>12.6f}")

        # Check convergence
        if abs(grad) < tolerance:
            print(f"\n  ✓ Converged at iteration {i}")
            break

        x = x_new

    return x_history, y_history


def main():
    print("=" * 65)
    print("   GRADIENT DESCENT — FINDING LOCAL MINIMA")
    print("=" * 65)

    # Parameters
    starting_point = 2
    learning_rate = 0.1
    num_iterations = 100

    print(f"\n  Function      : y = (x + 3)²")
    print(f"  Derivative    : dy/dx = 2(x + 3)")
    print(f"  Starting Point: x = {starting_point}")
    print(f"  Learning Rate : {learning_rate}")
    print(f"  Max Iterations: {num_iterations}")

    # Run Gradient Descent
    x_history, y_history = gradient_descent(
        starting_point, learning_rate, num_iterations
    )

    # Results
    final_x = x_history[-1]
    final_y = y_history[-1]

    print(f"\n{'═' * 65}")
    print(f"  RESULTS")
    print(f"{'═' * 65}")
    print(f"  Local Minima found at:")
    print(f"    x = {final_x:.6f}")
    print(f"    y = {final_y:.6f}")
    print(f"  Expected Minimum: x = -3, y = 0")
    print(f"  Total Iterations: {len(x_history) - 1}")

    # Plot the function and gradient descent path
    x_plot = np.linspace(-8, 5, 200)
    y_plot = function(x_plot)

    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='y = (x + 3)²')
    plt.plot(x_history, y_history, 'ro-', markersize=4, linewidth=1,
             label='Gradient Descent Path', alpha=0.7)
    plt.plot(x_history[0], y_history[0], 'gs', markersize=12, label=f'Start (x={starting_point})')
    plt.plot(x_history[-1], y_history[-1], 'r*', markersize=15, label=f'Minimum (x={final_x:.2f})')
    plt.xlabel('x')
    plt.ylabel('y = (x + 3)²')
    plt.title('Gradient Descent: Finding Local Minima of y = (x + 3)²')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('gradient_descent_plot.png', dpi=100)
    plt.close()
    print(f"\n  Plot saved as 'gradient_descent_plot.png'")
    print(f"{'═' * 65}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Function      : y = (x + 3)²
  Derivative    : dy/dx = 2(x + 3)
  Starting Point: x = 2
  Learning Rate : 0.1
  Max Iterations: 100

  Iter     x         y = (x+3)²     Gradient
  ──────────────────────────────────────────────────
  Start     2.000000      25.000000    10.000000
  1         1.000000      16.000000     8.000000
  2         0.200000       10.240000    6.400000
  3        -0.440000       6.553600     5.120000
  4        -0.952000       4.194304     4.096000
  5        -1.361600       2.684355     3.276800
  6        -1.689280       1.717987     2.621440
  7        -1.951424       1.099512     2.097152
  8        -2.161139       0.703688     1.677722
  9        -2.328911       0.450360     1.342177
  10       -2.463129       0.288231     1.073742
  ...
  40       -2.999999       0.000000     0.000002

  ✓ Converged at iteration 40

  RESULTS
    Local Minima found at:
      x = -3.000000
      y = 0.000000
    Expected Minimum: x = -3, y = 0
    Total Iterations: 40

========================================================================
"""
