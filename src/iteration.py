"""Module 4 - iterative solver starter.

Do not copy an update rule from another problem without verifying that it fits your assigned workbook.
"""

import math

from calculation import calculate_result
from validation import validate_inputs


def solve(
    *,
    target=None,
    initial_guess=None,
    tolerance=None,
    max_iterations=None,
    tank_height=None,
):
    """Return the solution status and a record of every diameter evaluated."""
    history = []

    def outcome(status, message, solution=None):
        last = history[-1] if history else None

        return {
            "status": status,
            "solution": solution,
            "result": last["result"] if last else None,
            "error": last["error"] if last else None,
            "iterations": len(history),
            "history": history,
            "message": message,
        }

    try:
        validate_inputs(
            target=target,
            initial_guess=initial_guess,
            tolerance=tolerance,
            max_iterations=max_iterations,
            tank_height=tank_height,
        )

        # Verify the first calculation before entering the iteration loop.
        first_volume = calculate_result(
            initial_guess, tank_height=tank_height
        )
    except ValueError as exc:
        return outcome("invalid_input", str(exc))

    guess = initial_guess
    lower = 0.0  # A mathematical bound, never a diameter we evaluate.
    upper = None

    for number in range(1, max_iterations + 1):
        try:
            volume = (
                first_volume
                if number == 1
                else calculate_result(guess, tank_height=tank_height)
            )
        except ValueError:
            return outcome(
                "not_converged",
                "No further finite volume could be evaluated.",
            )

        # Error is measured in ft³. Do not round before comparison.
        error = abs(volume - target)

        if not math.isfinite(error):
            return outcome(
                "not_converged",
                "The volume error is not finite.",
            )

        # Update the bounds according to this guess's volume.
        if volume < target:
            lower = guess
        elif volume > target:
            upper = guess

        history.append({
            "iteration": number,
            "guess": guess,          # ft
            "result": volume,        # ft³
            "target": target,        # ft³
            "error": error,          # ft³
            "lower_bound": lower,    # ft
            "upper_bound": upper,    # ft or None
        })

        if error <= tolerance:
            return outcome(
                "converged",
                "Volume is within tolerance.",
                guess,
            )

        if upper is None:
            # Find an upper diameter whose volume exceeds the target.
            next_guess = 2 * guess
        else:
            # Once the target is bracketed, test the midpoint.
            next_guess = (lower + upper) / 2

        if (
            not math.isfinite(next_guess)
            or next_guess <= 0
            or next_guess == guess
        ):
            return outcome(
                "not_converged",
                "No further distinct finite diameter is available.",
            )

        guess = next_guess

    return outcome(
        "not_converged",
        "Maximum number of iterations reached without convergence.",
    )
