import pytest

from iteration import solve
from validation import validate_inputs


VALID = dict(
    target=100.0,
    tank_height=5.0,
    initial_guess=3.0,
    tolerance=0.05,
    max_iterations=50,
)


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("initial_guess", -3.0),
        ("tank_height", 0.0),
        ("target", float("nan")),
        ("tolerance", 0.0),
        ("max_iterations", 0),
        ("max_iterations", True),
    ],
)
def test_invalid_input_is_refused_before_iteration(field, bad_value):
    inputs = VALID | {field: bad_value}
    result = solve(**inputs)

    assert result["status"] == "invalid_input"
    assert result["iterations"] == 0
    assert result["history"] == []
    assert result["solution"] is None
    assert field in result["message"]


def test_validation_function_can_be_tested_without_streamlit():
    with pytest.raises(ValueError, match="tank_height"):
        validate_inputs(**(VALID | {"tank_height": -1.0}))


def test_nonfinite_initial_volume_is_invalid_before_loop():
    # Each input is finite, but squaring a huge diameter overflows.
    result = solve(**(VALID | {"initial_guess": 1e308}))

    assert result["status"] == "invalid_input"
    assert result["iterations"] == 0
    assert result["history"] == []
    assert "volume" in result["message"]
