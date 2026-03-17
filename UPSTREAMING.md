# Upstreaming Candidates

These are suggestions only — no actual upstreaming has occurred.

## Included

### Theorem 1.9 — `product_formula`, `product_formula_all_primes`

```lean
theorem product_formula (q : ℚ) (hq : q ≠ 0) :
    |q| * ∏ p ∈ (q.num.natAbs * q.den).primeFactors, padicNorm p q = 1

theorem product_formula_all_primes (q : ℚ) (hq : q ≠ 0) :
    |q| * ∏ᶠ (p : ℕ) (_ : p.Prime), padicNorm p q = 1
```

**Justification:** Mathlib has a general product formula for number fields
(`NumberField.prod_abs_eq_one` in `Mathlib.NumberTheory.NumberField.ProductFormula`)
using infinite/finite places. However, there is no explicit ℚ-specific version
using `padicNorm` and the standard real absolute value. This formalization provides
a direct, elementary proof via the Fundamental Theorem of Arithmetic, which is
complementary to the general theory and useful pedagogically.

**Suggested Mathlib home:** `Mathlib.NumberTheory.Padics.ProductFormula`

### Lemma 1.4 — `nonarchimedean_iff_natCast_le_one`

```lean
theorem nonarchimedean_iff_natCast_le_one {k : Type*} [Field k]
    (f : AbsoluteValue k ℝ) :
    IsNonarchimedean f ↔ ∀ n : ℕ, f n ≤ 1
```

**Justification:** The forward direction exists in Mathlib as
`IsNonarchimedean.apply_natCast_le_one_of_isNonarchimedean`. For normed division
rings, the full iff is `isUltrametricDist_iff_forall_norm_natCast_le_one` in
`Mathlib.Analysis.Normed.Field.Ultra`, but that applies to norms/ultrametric
distance, not general `AbsoluteValue` maps. The reverse direction for
`AbsoluteValue k ℝ` (proved here via the binomial theorem) is not in Mathlib.

**Suggested Mathlib home:** `Mathlib.Algebra.Order.Ring.IsNonarchimedean`

### Corollary 1.5 — `posChar_isNonarchimedean`, `finite_field_absval_trivial`

```lean
theorem posChar_isNonarchimedean {k : Type*} [Field k] {p : ℕ} [CharP k p]
    (hp : p ≠ 0) (f : AbsoluteValue k ℝ) :
    IsNonarchimedean f

theorem finite_field_absval_trivial {k : Type*} [Field k] [Finite k]
    (f : AbsoluteValue k ℝ) (x : k) (hx : x ≠ 0) :
    f x = 1
```

**Justification:** Neither result exists in Mathlib. Part 1 uses Frobenius to
show `f(n)^p = f(n)` for all naturals, forcing `f(n) ≤ 1`, then applies
Lemma 1.4. Part 2 uses finite group theory (`orderOf`) to show `f(x)^n = 1`.
Both are standard textbook results about absolute values on fields of positive
characteristic.

**Suggested Mathlib home:** `Mathlib.Algebra.Order.AbsoluteValue.CharP` (new file)

### Example 1.24 — `Z_adjoin_sqrt5_not_integrally_closed`

```lean
theorem Z_adjoin_sqrt5_not_integrally_closed :
    ¬ IsIntegrallyClosed (Algebra.adjoin ℤ {Real.sqrt 5} : Subalgebra ℤ ℝ)
```

**Justification:** Mathlib has the general theory of integrally closed rings and
`ℤ[√d]` structures, but no concrete counterexample showing a specific quadratic
integer ring fails to be integrally closed. The proof constructs the golden ratio
φ = (1+√5)/2 as an element integral over ℤ (via φ²−φ−1 = 0) but not in ℤ[√5]
(via irrationality of √5). This is a natural counterexample for
`Mathlib.Counterexamples`.

**Suggested Mathlib home:** `Mathlib.Counterexamples.IntegralClosure`

### Example 1.29 — `half_one_plus_sqrt7_not_integral`

```lean
theorem half_one_plus_sqrt7_not_integral :
    ¬ IsIntegral ℤ ((1 + Real.sqrt 7) / 2 : ℝ)
```

**Justification:** Not in Mathlib. The proof shows the product
(1+√7)/2 · (1−√7)/2 = −3/2, which would need to be integral, but −3/2 ∉ ℤ
contradicts ℤ being integrally closed. This complements Example 1.24 by
illustrating the d mod 4 criterion: (1+√d)/2 is integral over ℤ iff d ≡ 1 (mod 4).

**Suggested Mathlib home:** `Mathlib.Counterexamples.IntegralClosure` (alongside Example 1.24)

## Excluded

| Item | Reason |
|------|--------|
| Definition 1.2 | Pure definition alias for `AbsoluteValue k ℝ` and `IsNonarchimedean` |
| Example 1.3 | Already in Mathlib as `AbsoluteValue.trivial` in `Mathlib.Algebra.Order.AbsoluteValue.Basic` |
| Definition 1.6 | Pure definition wrapper for equivalence of absolute values |
| Definition 1.7 | One-liners delegating to `IsAbsoluteValue.abv_eq_zero` and `padicNorm.nonarchimedean` |
| Theorem 1.8 | One-liner delegating to `Rat.AbsoluteValue.equiv_real_or_padic` (Ostrowski) |
| Definition 1.10 | Pure definition aliases for valuations, DVRs, and valuation rings |
| Definition 1.11 | Pure definition alias for `ValuationRing A` |
| Definition 1.12 | Pure definition alias for `IsLocalRing A` |
| Definition 1.13 | Pure definition alias for `IsLocalRing.ResidueField A` |
| Example 1.14 | Already in Mathlib: `IsLocalization.AtPrime.isDiscreteValuationRing_of_dedekind_domain` in `Mathlib.RingTheory.DedekindDomain.Dvr` |
| Example 1.15 | One-liner `inferInstance` for power series DVR |
| Theorem 1.16 | One-liner delegating to `IsDiscreteValuationRing.TFAE` |
| Definition 1.17 | Documentation examples for `IsIntegral` |
| Proposition 1.18 | One-liners delegating to `IsIntegral.add` and `IsIntegral.mul` |
| Definition 1.19 | Documentation examples for `integralClosure` and `IsIntegrallyClosed` |
| Proposition 1.20 | One-liner using `Algebra.IsIntegral.trans` |
| Corollary 1.21 | One-liner `inferInstance` for integral closure being integrally closed |
| Proposition 1.22 | One-liner `inferInstance` for ℤ being integrally closed |
| Corollary 1.23 | One-liner `inferInstance` for UFD being integrally closed |
| Proposition 1.25 | One-liner delegating to `IsIntegrallyClosed.of_equiv` for valuation rings |
| Definition 1.26 | Documentation examples for `NumberField` and `RingOfIntegers` |
| Proposition 1.28 | Already in Mathlib: `minpoly.isIntegrallyClosed_eq_field_fractions` in `Mathlib.FieldTheory.Minpoly.IsIntegrallyClosed` |
