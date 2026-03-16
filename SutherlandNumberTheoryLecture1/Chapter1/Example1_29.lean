import Mathlib.RingTheory.IntegralClosure.IsIntegral.Basic
import Mathlib.Data.Real.Sqrt

/-!
# Example 1.29: (1 + √7)/2 is not integral over ℤ

**Example 1.29.** We saw in Example 1.24 that (1 + √5)/2 is integral over ℤ.
Now consider α = (1 + √7)/2. Its minimal polynomial x² - x - 3/2 ∉ ℤ[x],
so α is not integral over ℤ.

This illustrates that whether (1 + √d)/2 is integral over ℤ depends on d mod 4:
it is integral when d ≡ 1 (mod 4) (as with d = 5) but not when d ≡ 3 (mod 4)
(as with d = 7).
-/

namespace SutherlandNumberTheoryLecture1.Chapter1

/-- The element α = (1 + √7)/2 satisfies α² - α - 3/2 = 0. Since the minimal
polynomial has non-integer coefficients, α is not integral over ℤ. -/
theorem half_one_plus_sqrt7_minimal_poly :
    let α : ℝ := (1 + Real.sqrt 7) / 2
    α ^ 2 - α - 3 / 2 = 0 := by
  sorry

/-- Example 1.29: (1 + √7)/2 is not integral over ℤ. Its minimal polynomial
x² - x - 3/2 does not have integer coefficients. -/
theorem half_one_plus_sqrt7_not_integral :
    ¬ IsIntegral ℤ ((1 + Real.sqrt 7) / 2 : ℝ) := by
  sorry

end SutherlandNumberTheoryLecture1.Chapter1
