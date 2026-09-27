# Calculation Map 

## Problem purpose

Find the internal diameter of a cylindrical tank that provides a target volume of 100 ft³ when the height is fixed at 5 ft. Evaluate a proposed diameter, compare its calculated volume with the target, and adjust the diameter until the volume error is at most 0.05 ft³ or 50 iterations have been performed.

## Inputs and units
| Input | Unit | Valid range / rule | Source |
|---|---|---|---|
| Target internal volume | ft³ | 100 ft³ in the training scenario; must be positive and finite for a general tool | Training scenario; positivity is a physical validation assumption |
| Fixed internal height | ft | 5 ft in the training scenario; must be positive and finite | Training scenario; positivity is a physical validation assumption |
| Starting diameter guess | ft | 3 ft in the training scenario; must be positive and finite | Training scenario; positivity is a physical validation assumption |
| Convergence tolerance | ft³ | 0.05 ft³; must be positive and finite | Training scenario; positivity is a solver validation rule |
| Maximum iterations | count | 50; must be a positive integer | Training scenario; integer restriction is a solver validation rule |

## Output / target

- **Target:** internal cylinder volume of 100 ft³.
- **One-pass output:** calculated internal volume in ft³ for a proposed diameter.
- **Final output:** diameter in ft only when the solver converges; also report the calculated volume, absolute volume error (ft³), status (CONVERGED / NOT CONVERGED / INVALID INPUT), number of iterations, and iteration history.
- **Convergence condition:** `abs(calculated_volume_ft3 - 100) <= 0.05` within at most 50 iterations. Do not require exact equality or present an unconverged diameter as a valid solution.

## Value adjusted during iteration

The proposed **internal tank diameter**, measured in feet, changes. The target volume (100 ft³) and height (5 ft) remain fixed. The training run starts at a proposed diameter of 3 ft.

## One-pass calculation steps
| Step | Operation | Output | Unit |
|---|---|---|---|
| 1 | Read one proposed internal diameter `d` and fixed internal height `h` | `d`, `h` | ft, ft |
| 2 | Calculate circular cross-sectional area: `A = π × (d / 2)²` | `A` | ft² |
| 3 | Calculate cylindrical volume: `V = A × h = π × d² × h / 4` | `V` | ft³ |
| 4 | Compare with target: `error = abs(V - target_volume)` | absolute error | ft³ |

For the first guess (`d = 3 ft`, `h = 5 ft`), `V ≈ 35.343 ft³`, so the error is approximately `64.657 ft³`. At `d = 5.046 ft`, `V ≈ 99.989 ft³` and the error is approximately `0.011 ft³`, which satisfies the training tolerance. These values are rounded for display; calculate convergence with unrounded values.

## Assumptions

- The tank is a right circular cylinder with a constant, unobstructed **internal** diameter and a fixed internal height.
- The target is usable internal volume; wall thickness, head geometry, fittings, fill level, and safety clearance are outside this example.
- All linear inputs use feet, the volume uses cubic feet, and π is used at normal floating-point precision.
- Diameter is positive. For positive height, the volume increases as diameter increases, which supports a bracketed bisection-style search if valid lower and upper diameter bounds are established.
- The one-pass calculation computes volume for one diameter; the update rule and iteration history belong to the solver, not the volume formula.

## Questions that still need verification

- What exact lower and upper diameter bounds and bracket-expansion rule does the training solver use? The description specifies a *bounded bisection-style* method but does not provide numerical bounds or its exact update rule.
