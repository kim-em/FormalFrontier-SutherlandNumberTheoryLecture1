import Mathlib.NumberTheory.Padics.PadicNorm
import Mathlib.Data.Nat.Factorization.Basic

/-!
# Theorem 1.9: Product Formula

**Theorem 1.9** (Product Formula). For every x ∈ ℚ× we have
  ∏_{p ≤ ∞} |x|_p = 1.

The product is over all places of ℚ: the real absolute value and the p-adic
absolute values for each prime p. For any nonzero rational, only finitely many
p-adic absolute values differ from 1, so the product is well-defined.
-/

namespace SutherlandNumberTheoryLecture1.Chapter1

/-- For a nonzero rational, padicNorm p q = 1 for all primes p not dividing
the numerator or denominator. -/
theorem padicNorm_eq_one_of_not_dvd (q : ℚ) (hq : q ≠ 0) (p : ℕ)
    (hp : Nat.Prime p) (hp_ndvd : p ∉ (q.num.natAbs * q.den).primeFactors) :
    padicNorm p q = 1 := by
  sorry

/-- Theorem 1.9 (Product Formula): For any nonzero rational q, the product of the
real absolute value and all p-adic absolute values equals 1:
  |q| * ∏_{p | num(q) * den(q)} |q|_p = 1
where |q| is the usual (archimedean) absolute value and the product ranges over
primes dividing the numerator or denominator. -/
theorem product_formula (q : ℚ) (hq : q ≠ 0) :
    |q| * ∏ p ∈ (q.num.natAbs * q.den).primeFactors, padicNorm p q = 1 := by
  sorry

end SutherlandNumberTheoryLecture1.Chapter1
