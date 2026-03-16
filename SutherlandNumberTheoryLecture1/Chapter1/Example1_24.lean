import Mathlib.RingTheory.IntegralClosure.IntegrallyClosed
import Mathlib.RingTheory.Adjoin.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.RingTheory.IntegralClosure.IsIntegral.Basic

/-!
# Example 1.24: Z[√5] is not integrally closed

**Example 1.24.** The ring Z[√5] is not a UFD (nor a PID) because it is not
integrally closed: consider φ = (1 + √5)/2 ∈ Frac Z[√5], which is integral
over Z (and hence over Z[√5]), since φ² - φ - 1 = 0. But φ ∉ Z[√5], so Z[√5]
is not integrally closed.
-/

namespace SutherlandNumberTheoryLecture1.Chapter1

/-- The golden ratio φ = (1 + √5)/2 satisfies φ² - φ - 1 = 0,
hence is integral over ℤ. -/
theorem golden_ratio_integral :
    let φ : ℝ := (1 + Real.sqrt 5) / 2
    φ ^ 2 - φ - 1 = 0 := by
  sorry

/-- The golden ratio φ = (1 + √5)/2 is not in ℤ[√5].
Elements of ℤ[√5] have the form a + b√5 for a, b ∈ ℤ,
but φ = 1/2 + (1/2)√5 has non-integer coefficients. -/
theorem golden_ratio_not_in_Z_adjoin_sqrt5 :
    (1 + Real.sqrt 5) / 2 ∉ (Algebra.adjoin ℤ {Real.sqrt 5} : Subalgebra ℤ ℝ) := by
  sorry

/-- Example 1.24: ℤ[√5] is not integrally closed. The golden ratio φ = (1 + √5)/2
is integral over ℤ (satisfying φ² - φ - 1 = 0) but does not lie in ℤ[√5]. -/
theorem Z_adjoin_sqrt5_not_integrally_closed :
    ¬ IsIntegrallyClosed (Algebra.adjoin ℤ {Real.sqrt 5} : Subalgebra ℤ ℝ) := by
  sorry

end SutherlandNumberTheoryLecture1.Chapter1
