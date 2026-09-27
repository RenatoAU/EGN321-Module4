"""Module 4 - iterative solver starter.

Do not copy an update rule from another problem without verifying that it fits your assigned workbook.
"""

def solve(*, target, initial_guess, tolerance, max_iterations, **engineering_inputs):
    if tolerance <= 0:
        raise ValueError("tolerance must be greater than 0")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be greater than 0")

    history = []
    guess = initial_guess

    for iteration in range(1, max_iterations + 1):
        # TODO 1: calculate the current engineering result.
        # TODO 2: calculate error relative to target.
        # TODO 3: append iteration evidence to history.
        # TODO 4: return CONVERGED when error <= tolerance.
        # TODO 5: update guess using a method that fits your assigned problem.
        raise NotImplementedError("Complete the iterative solver using your verified calculation.")

    return {
        "status": "not_converged",
        "solution": None,
        "iterations": max_iterations,
        "history": history,
    }
