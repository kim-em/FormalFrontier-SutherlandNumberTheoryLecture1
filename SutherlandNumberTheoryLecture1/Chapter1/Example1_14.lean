import Mathlib.RingTheory.Localization.AtPrime.Basic
import Mathlib.RingTheory.DiscreteValuationRing.Basic
import Mathlib.RingTheory.LocalRing.ResidueField.Defs
import Mathlib.Data.ZMod.Basic
import Mathlib.RingTheory.Int.Basic

/-!
# Example 1.14: Z_(p) as a DVR

**Example 1.14.** For the p-adic valuation v_p : ℚ → ℤ ∪ {∞} we have the valuation ring

  ℤ_(p) := {a/b : a, b ∈ ℤ, p ∤ b},

with maximal ideal 𝔪 = (p); this is the *localization* of the ring ℤ at the prime
ideal (p). The residue field is ℤ_(p)/pℤ_(p) ≅ ℤ/pℤ ≅ 𝔽_p.

In Mathlib, `Localization.AtPrime (Ideal.span {(p : ℤ)})` gives ℤ_(p).
The ideal `Ideal.span {(p : ℤ)}` is prime when p is a prime number.
-/

namespace SutherlandNumberTheoryLecture1.Chapter1

/-- Example 1.14: The localization ℤ_(p) is a DVR.
For a prime p, the localization of ℤ at the prime ideal (p) is a discrete
valuation ring with maximal ideal (p) and residue field 𝔽_p. -/
theorem localization_at_prime_is_dvr (p : ℕ) [hp : Fact (Nat.Prime p)]
    (I : Ideal ℤ) [hI : I.IsPrime] (hIp : I = Ideal.span {(p : ℤ)}) :
    IsDiscreteValuationRing (Localization.AtPrime I) := by
  sorry

/-- The residue field of ℤ_(p) is isomorphic to ℤ/pℤ. -/
theorem localization_at_prime_residue_field (p : ℕ) [hp : Fact (Nat.Prime p)]
    (I : Ideal ℤ) [hI : I.IsPrime] (hIp : I = Ideal.span {(p : ℤ)}) :
    Nonempty (IsLocalRing.ResidueField (Localization.AtPrime I) ≃+* ZMod p) := by
  sorry

end SutherlandNumberTheoryLecture1.Chapter1
