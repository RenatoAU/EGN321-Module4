# Module 4 Iterative Sizing Tool

## Project Overview

This Python and Streamlit tool searches for the internal diameter of a cylindrical tank that reaches a requested internal volume at a fixed height. It evaluates one diameter at a time, keeps a record of each attempt, and reports **CONVERGED**, **NOT CONVERGED**, or **INVALID INPUT**. The engineering calculation is separate from the web interface so it can be tested without starting Streamlit.

**Source limitation:** The available spreadsheet, `EGN321_Module4_Assignment4_1_Tank_GoalSeek_Training_Example.xlsx`, calls itself a *synthetic training example* in cell A2. This project follows that workbook. Confirm with the instructor that this example is acceptable for the graded submission before presenting it as the assigned engineering workbook.

## Original Workbook / Process

The `Goal Seek Example` worksheet records a target volume of **100 ft³** (`B5`), fixed tank height of **5 ft** (`B6`), starting diameter of **3 ft** (`B7`), volume tolerance of **0.05 ft³** (`B8`), and an intended maximum of **50 iterations** (`B9`). Cells `E5:E11` contain seven manually entered diameter guesses. Formulas in `F5:F11` calculate volumes, `G5:G11` calculate absolute errors, and `H5:H11` mark each guess `YES` when its error is at most the tolerance. The last manual guess, 5.046 ft, is accepted.

The spreadsheet does not calculate the next guess or enforce its 50-iteration value. The Python program automates both tasks using the update method documented below.

## Inputs and Units

| Input | Unit | Default in app | Rule |
|---|---|---:|---|
| Target volume | ft³ | 100 | Positive, finite number |
| Tank height | ft | 5 | Positive, finite number; fixed during a run |
| Starting internal diameter | ft | 3 | Positive, finite number |
| Volume tolerance | ft³ | 0.05 | Positive, finite absolute error |
| Maximum iterations | evaluations | 50 | Positive integer |

The program returns the final diameter in ft only if it converges. Volume and absolute error are reported in ft³.

## Iterative Calculation

`calculation.py` evaluates one diameter `d` at a fixed height `h` using the workbook formula:

```text
volume_ft3 = π × diameter_ft² × height_ft / 4
```

`iteration.py` evaluates the starting diameter, then searches for an interval containing the target: when the starting volume is low, it doubles the diameter until the volume reaches or exceeds the target; when the starting volume is high, it uses zero as a mathematical lower bound without evaluating zero as a tank diameter. Once it has lower and upper bounds, it evaluates their midpoint and narrows the interval after each attempt. Every volume evaluation counts as an iteration. This update method is a software design choice because the workbook's guesses are manual.

## Starting Condition

The workbook example starts at a diameter of **3 ft** with a fixed **5 ft** height. The app lets the user enter a different positive starting diameter and height. The starting guess is evaluated and stored as iteration 1.

## Convergence Rule

```text
absolute_error_ft3 = abs(calculated_volume_ft3 - target_volume_ft3)
CONVERGED if absolute_error_ft3 <= tolerance_ft3
```

The `<=` matches the workbook's `H5:H11` formulas. The decision uses unrounded numbers; displayed values may be rounded.

## Tolerance

The default tolerance is **0.05 ft³**. For a target of 100 ft³, a calculated volume from 99.95 through 100.05 ft³, inclusive, satisfies the rule. This tolerance measures volume error, not diameter error or percent error.

## Maximum Iterations

The default limit is **50 evaluated guesses**, including guesses used to find an upper bound. The solver stops at that limit even if it has not found an acceptable diameter. With the default inputs, the implemented search converges at **5.04638671875 ft** on iteration **13**, with a volume error of approximately **0.00482243 ft³**. It takes a different path from the workbook's seven manual guesses.

## Validation Rules

`validation.py` rejects missing, nonnumeric, nonfinite, zero, or negative target volume, height, starting diameter, or tolerance. Maximum iterations must be an integer of at least 1; Boolean values are rejected. The starting diameter is also checked for a finite calculated volume before iteration starts. Error messages identify the invalid field where possible.

These are proposed software rules based on the cylinder model. The workbook does not document upper engineering operating ranges or enforce these rules itself.

## Non-Convergence Behavior

If the inputs are valid but the tolerance is not met before the evaluation limit, the solver returns **NOT CONVERGED**, keeps the attempted history and last volume/error, and returns no valid solution diameter. It also reports non-convergence if no further distinct finite diameter can be evaluated. **INVALID INPUT** happens before the loop and has zero iterations and an empty history.

## Iteration History

The app displays the iteration number, diameter guess (ft), calculated volume (ft³), target volume (ft³), absolute error (ft³), and the current lower and upper diameter bounds (ft). The history is available after both successful and unsuccessful valid runs.

## Testing

Automated tests cover workbook volume calculations, two convergence starting conditions, an exact tolerance boundary, non-convergence, iteration history, iteration limits, invalid inputs, and the generated-version defect. In the checked project snapshot, running `python -m pytest -q -rx tests` produced **15 passed, 1 xfailed**. The `xfail` is intentional evidence about the separate AI implementation, not a failure in the primary solver.

## AI-Generated Version

ChatGPT generated an independent Newton-style candidate in `ai_generated_iteration.py`. It is kept separate and is **not** called by `app.py`. The project records AI use and verification in `AI_LOG.md`; no Ollama run is claimed.

## Generated-Version Defect

The workbook accepts `error <= tolerance`, but `ai_generated_iteration.py` checks `error < tolerance`. With an initial error exactly equal to 0.5 ft³ and a tolerance of 0.5 ft³, the primary solver correctly reports convergence on its first evaluation while the alternative incorrectly reports non-convergence. `tests/test_generated_version.py` reproduces this defect as a strict expected failure without changing the alternative code.

## Ollama / AI Use

ChatGPT was used to review the workbook and assignment, draft the iteration plan and Python files, and propose tests. Suggested behavior was checked against workbook cells and by running the Python tests. See `AI_LOG.md` for the prompts, what was used, and remaining review tasks. The supplied Ollama notebook is optional learning material; this project does not claim to have run Ollama.

## Assumptions

- The tank is a right circular cylinder; `d` and `h` represent internal dimensions.
- Height stays fixed while diameter changes, and all dimensions are in feet.
- The one-pass formula uses π at Python floating-point precision.
- A zero diameter is used only as a lower mathematical search bound, never as a valid evaluated diameter.
- A positive height makes calculated volume increase with positive diameter, enabling the bracketed search.

## Known Limitations

- This implementation follows a **training workbook**, whose acceptability for the graded project has not been confirmed.
- It does not model wall thickness, tank heads, obstructions, fittings, partial fill, manufacturing limits, or safety margins.
- The workbook does not specify maximum physical diameter/height or a required next-guess rule; the software method is documented in `ITERATION_PLAN.md`.
- Very large or small values can exceed practical floating-point precision. The software rejects nonfinite starting volumes and does not label a stalled search as a valid solution.

## How to Run Locally

Use Python 3.10 or newer. Put `app.py`, `calculation.py`, `validation.py`, `iteration.py`, `ai_generated_iteration.py`, and `requirements.txt` in the repository root, with the three test files in `tests/`. From the repository root:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

To run the automated tests in a separate terminal:

```bash
python -m pytest -q -rx tests
```

The app does not require the Excel file at runtime; its verified formula is implemented in `calculation.py`. Keep the workbook name and cell references in the documentation so the origin of the calculation is clear.

## Live Streamlit Application

**Pending deployment.** Replace this line with the working public Streamlit URL after publishing the GitHub repository and deploying `app.py`. Open the URL in a browser outside the development environment and check a converged case, a non-converged case, and an invalid input before submitting it.
