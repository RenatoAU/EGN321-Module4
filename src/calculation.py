"""Module 4 - deterministic engineering calculation.

Replace TODO items using the assigned workbook.
"""
import math
from numbers import Real


def calculate_result(adjusted_value, *, tank_height):
    """Return volume in ft³ for a diameter and height measured in ft."""
    for name, value in (
        ("adjusted_value", adjusted_value),
        ("tank_height", tank_height),
    ):
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{name} must be a number in feet")
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be positive and finite")

    try:
        # Same formula as the workbook: PI() * diameter^2 / 4 * height
        volume = (math.pi / 4) * adjusted_value**2 * tank_height
    except OverflowError as exc:
        raise ValueError(
            "calculated volume is not finite for these inputs"
        ) from exc

    if not math.isfinite(volume):
        raise ValueError("calculated volume is not finite for these inputs")

    return volume
