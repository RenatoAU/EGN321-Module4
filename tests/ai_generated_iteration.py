"""Independent ChatGPT-generated Newton-style candidate for review.

Kept separate from iteration.py so its behavior can be tested without
changing the application's verified solver.
"""

import math


def ai_solve(*, target, initial_guess, tank_height, tolerance, max_iterations):
    guess = initial_guess

    for number in range(1, max_iterations + 1):
        volume = math.pi * guess**2 * tank_height / 4
        error = abs(volume - target)

        if error < tolerance:
            return {
                "status": "converged",
                "solution": guess,
                "error": error,
                "iterations": number,
            }

        slope = math.pi * tank_height * guess / 2

        if slope == 0:
            return {
                "status": "not_converged",
                "solution": None,
                "error": error,
                "iterations": number,
            }

        guess += (target - volume) / slope

    return {
        "status": "not_converged",
        "solution": None,
        "error": error,
        "iterations": max_iterations,
    }
