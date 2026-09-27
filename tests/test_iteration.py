import math

import pytest

from calculation import calculate_result
from iteration import solve


WORKBOOK = dict(
    target=100.0,
    tank_height=5.0,
    tolerance=0.05,
    max_iterations=50,
)


def test_one_pass_volume_matches_first_workbook_row():
    # Goal Seek Example!E5 = 3 ft; F5 displays approximately 35.343 ft³.
    assert calculate_result(3.0, tank_height=5.0) == pytest.approx(
        35.34291735288517
    )


def test_workbook_accepted_guess_converges_on_first_evaluation():
    # E11 = 5.046 ft is an accepted manual guess (H11 = YES).
    result = solve(**WORKBOOK, initial_guess=5.046)

    assert result["status"] == "converged"
    assert result["solution"] == 5.046
    assert result["iterations"] == 1
    assert result["error"] <= WORKBOOK["tolerance"]


def test_different_starting_diameter_converges():
    # Starting from B7 = 3 ft follows our documented update rule.
    result = solve(**WORKBOOK, initial_guess=3.0)

    assert result["status"] == "converged"
    assert result["history"][0]["guess"] == 3.0
    assert result["iterations"] > 1
    assert result["error"] <= WORKBOOK["tolerance"]
    assert result["result"] == pytest.approx(100.0, abs=0.05)


def test_tolerance_boundary_is_inclusive():
    initial_volume = calculate_result(2.0, tank_height=1.0)
    target = initial_volume + 0.5

    assert abs(initial_volume - target) == 0.5

    result = solve(
        target=target,
        tank_height=1.0,
        initial_guess=2.0,
        tolerance=0.5,
        max_iterations=1,
    )

    assert result["status"] == "converged"
    assert result["error"] == 0.5
    assert result["iterations"] == 1


def test_valid_input_can_fail_to_converge():
    result = solve(
        **(WORKBOOK | {"max_iterations": 1}),
        initial_guess=3.0,
    )

    assert result["status"] == "not_converged"
    assert result["solution"] is None
    assert result["error"] > WORKBOOK["tolerance"]


def test_history_records_real_results_and_errors():
    result = solve(**WORKBOOK, initial_guess=3.0)

    assert len(result["history"]) == result["iterations"]
    assert [row["iteration"] for row in result["history"]] == list(
        range(1, result["iterations"] + 1)
    )
    assert result["history"][0]["result"] == pytest.approx(
        35.34291735288517
    )
    assert result["history"][1]["guess"] == 6.0

    for row in result["history"]:
        assert row["result"] == pytest.approx(
            math.pi * row["guess"] ** 2 * 5.0 / 4
        )
        assert row["error"] == pytest.approx(
            abs(row["result"] - 100.0)
        )


def test_maximum_iterations_counts_every_evaluated_guess():
    result = solve(
        **(WORKBOOK | {"max_iterations": 2}),
        initial_guess=3.0,
    )

    assert result["status"] == "not_converged"
    assert result["iterations"] == 2
    assert len(result["history"]) == 2
    assert [row["guess"] for row in result["history"]] == [3.0, 6.0]
    assert result["solution"] is None
