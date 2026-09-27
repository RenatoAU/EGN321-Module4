"""Module 4 - input validation.

Validation should happen before the iterative solver begins.
"""

import math
from numbers import Integral, Real


def validate_inputs(
    *,
    target=None,
    initial_guess=None,
    tolerance=None,
    max_iterations=None,
    tank_height=None,
):
    """Raise ValueError for an invalid input; otherwise return True."""
    for name, value in (
        ("target", target),
        ("tank_height", tank_height),
        ("initial_guess", initial_guess),
        ("tolerance", tolerance),
    ):
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must be a number greater than zero")
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be positive and finite")

    if (
        isinstance(max_iterations, bool)
        or not isinstance(max_iterations, Integral)
        or max_iterations < 1
    ):
        raise ValueError("max_iterations must be a positive integer")

    return True
