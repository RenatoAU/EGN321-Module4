# AI Use Log 

**AI tool:** ChatGPT (model name not recorded in the project).  
**Project source reviewed:** `EGN321_Module4_Assignment4_1_Tank_GoalSeek_Training_Example.xlsx`.

I used ChatGPT as a coding and review assistant while working through the Module 4 starter files. Its help included more than definitions: it drafted an iteration plan, Python modules, a Streamlit interface, and candidate tests. I kept the workbook formula as the source for the one-pass calculation and tested the suggested software behavior. The workbook labels itself a **training example**; I still need to confirm whether it is acceptable for the graded project.

| Date | Tool / model | Purpose and prompt summary | Used / modified / rejected | Verification method | Result |
|---|---|---|---|---|---|
| 2026-09-27 | ChatGPT / model not recorded | “Explain the assignment and identify what belongs in the GitHub repository.” | Used the project organization and requirement checklist as guidance. | Compared the suggestions with the assignment description, starter package, and submission checklist. | Identified the separate calculation, validation, iteration, UI, test, and documentation files. |
| 2026-09-27 | ChatGPT / model not recorded | “Complete the Calculation Map using the supplied tank workbook, including its inputs, units, target, and formula.” | Modified the first draft after checking the actual workbook; kept explicit cell references and the training-example label. | Inspected `B5:B9` and formulas in `F5:H11`; separately calculated the first and accepted example volumes. | Verified `V = πd²h/4` in ft³, `error = abs(V − target)` in ft³, and the workbook's inclusive `error <= tolerance` rule. |
| 2026-09-27 | ChatGPT / model not recorded | “Suggest a repeatable way to adjust diameter because the sheet contains manually entered guesses.” | Used bracket expansion followed by bisection in the iteration plan and solver. This is a software design choice, not a formula taken from the workbook. | Checked that volume increases with diameter for positive height and compared the solver's result against the target and tolerance. | With target 100 ft³, height 5 ft, and a 3 ft start, the proposed method converged in 13 evaluated guesses with an error of about 0.00482 ft³. |
| 2026-09-27 | ChatGPT / model not recorded | “Draft the one-pass calculation, input validation, and iterative solver as separate Python files.” | Used the generated drafts as the working implementation; reviewed them against the Calculation Map and Iteration Plan. | Ran the one-pass example and checked converged, non-converged, and invalid-input outcomes using Python. | `calculation.py`, `validation.py`, and `iteration.py` produce distinct statuses and record evaluated guesses. |
| 2026-09-27 | ChatGPT / model not recorded | “Connect the tested solver to the Streamlit starter interface and display inputs, units, status, result, error, and history.” | Used the drafted `app.py`. | Checked Python syntax and simulated the interface for all three statuses. | The simulated app displayed CONVERGED, NOT CONVERGED, and INVALID INPUT appropriately. A real browser run remains to be checked. |
| 2026-09-27 | ChatGPT / model not recorded | “Suggest meaningful tests for both successful and unsuccessful paths, plus an AI-generated implementation to challenge.” | Used the proposed tests and kept the alternative implementation separate from the primary solver. | Ran `python -m pytest -q -rx tests` and inspected the reported outcomes. | 15 tests passed and one generated-version test was marked as an expected failure. |
| 2026-09-27 | ChatGPT / model not recorded | “Produce an independent alternative iterative solver for the same cylinder equation so I can test it.” | Kept `ai_generated_iteration.py` unchanged before writing the defect test; did not use it in the Streamlit application. | The boundary test sets the initial error to exactly 0.5 ft³ with a tolerance of 0.5 ft³ and permits one evaluation. | The workbook and primary solver accept equality (`<=`), but the AI alternative uses `<` and incorrectly reports non-convergence. `test_generated_version.py` records this as a strict `xfail`. |

## What the AI version got wrong

In `Goal Seek Example!H5:H11`, the acceptance formula uses `<=`. The alternative AI code used `<`, so it rejects a guess whose error is exactly the permitted tolerance. The automated test demonstrates the mismatch without editing the AI-generated file. An `xfail` in pytest is expected evidence of this particular defect; a new failure in the primary solver would require investigation.

## My review before submission

- Read each Python file and confirm that its inputs, units, and status messages match the Calculation Map.
- Run the full test suite in my own GitHub checkout and inspect the `xfail` reason; do not treat a skipped test as a pass.
- Run `streamlit run app.py` locally, try a converged case, a one-iteration non-converged case, and an invalid input, and inspect the displayed history.
- Confirm with the instructor whether the provided training workbook may be used for the graded project. If a different workbook is assigned, revise the calculation, assumptions, tests, and documentation before submission.
