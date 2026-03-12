# Theory: Möbius Galton Board

## The Setup

A classical Galton board has W columns and H rows of offset pegs. A ball dropped
from the top takes a random ±1 step at each peg. In a standard board, the left
and right walls reflect. In a cylinder board, they wrap (periodic BCs). In the
**Möbius board**, they wrap with a **ℤ₂ parity flip** on every crossing:

```
(x = W, parity p)  →  (x = 0, parity 1−p)
(x = −1, parity p) →  (x = W−1, parity 1−p)
```

This is the defining antiperiodic (Möbius) boundary condition.

## Parity Observable

Every ball starts at even parity (p=0). We track:

```
α₊(W, H) = Pr[final parity = 0]
```

**Key result:**

```
α₊(W, H) = ½ [1 + cosᴴ(π/W)]
```

## Derivation: Transfer Matrix

Label a state by (x, p) with x ∈ {0,…,W−1}, p ∈ {0,1}. The state space is
W×2 dimensional.

### Fourier Analysis on the Antiperiodic Lattice

For the cylinder board, the transfer matrix T₀ has eigenvectors e^{2πikx/W}
with eigenvalues λₖ = cos(2πk/W).

The Möbius seam changes boundary conditions from periodic to **antiperiodic**:
ψ(x+W) = −ψ(x). This shifts the allowed momenta from k = 0,1,…,W−1 to
**half-integer** values k = ½, 3/2, …, (2W−1)/2, giving eigenvalues:

```
μₖ = cos((2k+1)π/W)   for k = 0, 1, ..., W−1
```

### Leading Eigenvalue

The largest eigenvalue (closest to 1) in the antiperiodic sector is:

```
μ₀ = cos(π/W)
```

Starting from even parity at x=0, the even-parity probability after H steps is:

```
α₊(W, H) = ½ [1 + μ₀ᴴ] = ½ [1 + cosᴴ(π/W)]
```

The ½ comes from the equal weight of even/odd sectors in the initial state
projection onto antiperiodic eigenvectors.

## Phase Transition at k*

As W increases, cos(π/W) → 1, so α₊ → 1 (strong parity selectivity).
As W decreases toward 2, cos(π/2) = 0, so α₊ → ½ (no parity selectivity).

The **phase transition** is defined by α₊ = k* = 1/(2 ln 2) ≈ 0.7213.

**Why k*?** The information-theoretic interpretation: k* is the maximum
entropy threshold for a binary channel. Above k*, even parity is the
"majority" in an information-theoretic sense. Below k*, the channel is
too mixed to distinguish parity.

This is not a symmetry-breaking transition in the usual sense — it is a
**spectral gap threshold**: the gap between the leading and next-leading
antiperiodic eigenvalues crosses a critical value at W = Wₑ.

## Critical Width Scaling

Setting α₊ = k* and solving for W:

```
½ [1 + cosᴴ(π/Wₑ)] = k*
cosᴴ(π/Wₑ) = 2k* − 1 = 1/ln(2) − 1 ≈ 0.4427
cos(π/Wₑ) = [1/ln(2) − 1]^(1/H)
Wₑ = π / arccos([1/ln(2) − 1]^(1/H))
```

For large H, expanding: arccos(x) ≈ π/2 for x near 0, and using
`[1 − 1/ln2]^{1/H} ≈ exp(−ln(ln2)/H)`:

```
Wₑ ≈ π √(H / ln(1/(2k*−1))) ≈ 2.46 √H
```

The constant 2.46 = π/√(ln(1/0.4427)) = π/√(ln 2.26) emerges from the
information-theoretic value of k*.

## Parity Projectors

The clean factorisation into even/odd sectors is exact because the Möbius
boundary condition is a **global** (non-local) constraint that commutes with
the local stepping rule. The parity projectors

```
P₊ = ½(1 + σz)   (even sector)
P₋ = ½(1 − σz)   (odd sector)
```

commute with T for all W, H. This is the algebraic reason α₊ takes a clean
closed form — there is no mixing between parity sectors except at seam crossings.
