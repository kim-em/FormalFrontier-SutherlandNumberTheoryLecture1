---
name: proof-polish
description: Use when running Stage 3.4 (Proof Polishing) to bring sorry-free proofs to Mathlib quality. Use when assessing whether a proof needs cleanup, when working through proof-polish GitHub issues, or when deciding which tactic to prefer for a given goal.
allowed-tools: Read, Edit, Bash, Glob, Grep
---

# Proof Polishing for FormalFrontier

This skill guides Stage 3.4: bringing all sorry-free proofs to Mathlib quality. Work through proofs systematically — triage first, automated cleanup second, manual polish per issue.

## Phase 1: Triage

For each sorry-free Lean file:
1. Run `lake build 2>&1 | tee /tmp/polish-build.log` and capture all linter warnings
2. Read each non-trivial proof and assess against the quality checklist below
3. Open one GitHub issue labelled `proof-polish` per proof that needs attention, describing specifically what needs fixing

**Trivial proofs** (single `rfl`, `trivial`, `inferInstance`, `decide`, one-line `exact`) don't need issues unless they have linter warnings.

## Phase 2: Automated Cleanup (run before manual polish)

Apply these bulk transformations first, verifying `lake build` after each batch:

- **Trailing semicolons**: Remove `;` at end of terminal tactic lines (`aesop;` → `aesop`)
- **Whitespace in brackets**: `( foo )` → `(foo)`, `[ foo ]` → `[foo]`
- **`refine'` → `refine`**: Replace all `refine'` with `refine`, then verify build (refine' is deprecated)
- **Non-Mathlib simp flags**: Remove `+decide`, `+contextual`, `+zetaDelta` from `simp` calls
- **Unused simp lemmas**: Remove simp arguments that Lean warns are unnecessary ("simp made no progress" / "unnecessary simp lemma")

Commit automated changes separately from manual changes.

## Phase 3: Manual Polish (per issue)

For each `proof-polish` issue:
1. Reproduce the problem locally
2. Apply fixes one at a time; verify `lake build` after each change
3. Commit and close the issue with `Fixes #N`; enable auto-merge on the PR

## Quality Checklist

### Linter
- [ ] `lake build` produces zero warnings for this file

### `simp` discipline
- [ ] **Non-terminal `simp`** (i.e., `simp` followed by more tactics): replace with `simp only [...]` using the minimal lemma set from `simp?`
- [ ] **Terminal `simp`** (i.e., `simp` closes the goal): keep as bare `simp` — listing every lemma is obfuscatory

### Dead code
- [ ] No unused `have`, `obtain`, or local `let`
- [ ] No commented-out tactic attempts

### Arithmetic and algebra
- [ ] **Linear arithmetic**: use `lia` (prefer over `omega` for arithmetic goals)
- [ ] **Commutative ring identities**: use `ring`
- [ ] **Nonlinear arithmetic**: use `nlinarith` or `polyrith`
- [ ] **Numeric computations**: use `norm_num`
- [ ] **Positivity goals** (`0 < f x`, `0 ≤ f x`): use `positivity`
- [ ] **Numeric coercions** (goals with `↑`, `Nat.cast`, `Int.cast`, etc.): use `norm_cast` or `push_cast` to normalize first

### Automation passes
- [ ] **`grind` pass**: try replacing a terminal chain of proof steps with `grind`. If bare `grind` fails, add the theorem names referenced in those steps as arguments: `grind [Theorem.foo, lemma_bar]`. If it still fails, try adding `@[simp]` or `@[ext]` annotations to relevant definitions/lemmas that would help `grind` or `ext; simp` go through.
- [ ] **`fun_prop`**: for goals asserting continuity, measurability, or differentiability of a function
- [ ] **`gcongr`**: for congruence goals (replacing parts of an expression)
- [ ] **`decide`**: for finite decidable goals

### Avoiding fragile tactics
- [ ] **No `erw`**: replace with `rw` plus appropriate coercions, `norm_cast`, or a restatement of the goal
- [ ] **No `convert` relying on non-trivial definitional equality**: prefer rewriting the proof to directly establish the goal. Use `convert` only when the goals differ by superficial syntactic differences, not when they require non-trivial unification.

### Style
- [ ] No `refine'` — use `refine` (or `exact`)
- [ ] Multi-step equalities/inequalities: consider `calc` blocks when intermediate steps clarify the argument
- [ ] Tactic chains that chain logically (each step sets up the next) should be on separate lines rather than joined with `;`, except for trivially short patterns like `intro x; exact ...`

## Common Patterns

### Replacing a tactic chain with `grind`

Before:
```lean
  have h1 : a ∣ b := dvd_of_eq hab
  have h2 : b ∣ c := dvd_trans h1 hbc
  exact dvd_trans h1 h2
```
Try:
```lean
  grind [dvd_of_eq, dvd_trans]
```

### Non-terminal `simp only` conversion

Before:
```lean
  simp at h
  exact h.2
```
Run `simp?` to find the minimal set, then:
```lean
  simp only [Prod.fst, Prod.snd] at h
  exact h.2
```

### `norm_cast` for coercion goals

Before:
```lean
  have : (n : ℤ) = (m : ℤ) := by exact_mod_cast h
  exact_mod_cast this
```
After:
```lean
  exact_mod_cast h
```

### Replacing `erw` with `rw` + coercion

Before:
```lean
  erw [Nat.cast_mul]
```
Try:
```lean
  push_cast
  rw [Nat.cast_mul]
```
or just `norm_cast` if the whole goal is a coercion identity.
