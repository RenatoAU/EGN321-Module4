import pytest

from ai_generated_iteration import ai_solve
from calculation import calculate_result
from iteration import solve


@pytest.mark.xfail(
    strict=True,
    reason="AI version uses < instead of <= at tolerance boundary",
)
def test_generated_version_accepts_exact_tolerance_boundary():
    # The workbook uses <= in H5, so equality must converge.
    target = calculate_result(2.0, tank_height=1.0) + 0.5

    values = dict(
        target=target,
        tank_height=1.0,
        initial_guess=2.0,
        tolerance=0.5,
        max_iterations=1,
    )

    assert solve(**values)["status"] == "converged"
    assert ai_solve(**values)["status"] == "converged"
