# Optical vs Quantum Versions

## Three Levels of Description

The Möbius Galton board can be realised at three levels of physical description,
all producing consistent results with the analytic formula.

---

## 1. Classical Monte Carlo

**Model:** N independent particles, each taking a random ±1 step at each row.
Parity flips on Möbius seam crossings.

**Result:** α₊(W, H) = ½[1 + cosᴴ(π/W)] — exact match.

**Error:** Statistical noise O(1/√N). For N=200,000, typical |MC − theory| < 0.001.

**Physical realisation:** Mechanical Galton board with parity beads.

---

## 2. Coherent Optical (Laser)

**Model:** Complex probability amplitudes propagate through beamsplitter grid.
At each peg: amplitude splits by 1/√2 (50:50 beamsplitter).
At Möbius seam: amplitude gains phase factor i (half-wave plate at 45°).

**Mathematical structure:**
```
ψ(x±1, p) += ψ(x, p) / √2      (interior pegs)
ψ(0, 1−p) += ψ(W, p) × i / √2  (seam crossing: phase i + parity flip)
```

**Result:** Even parity dominates **more strongly** than classical.
The effective phase boundary shifts to narrower W (the transition happens
at smaller boards). This is a coherent effect: constructive interference
reinforces the even sector.

**Key difference from classical:** The parity mixing is coherent (amplitude-level)
rather than incoherent (probability-level). This sharpens the transition.

**Physical realisation:** Beamsplitter cube grid + half-wave plate at seam.

---

## 3. Single-Photon Quantum Walk

**Model:** A single photon propagates as a quantum superposition. At each row,
a position-sensitive detector collapses the photon to a definite position
(Born-rule measurement), but does NOT measure parity. Parity remains coherent
between rows.

**Mathematical structure:**
- Within each row: coherent diffraction (same as optical)
- At row boundary: Born-rule position collapse → incoherent position mixing

**Result:** **Exact match** to classical Monte Carlo and analytic formula.
The position decoherence (Born-rule collapse) washes out the coherent
interference that makes the optical version sharper.

**Interpretation:** Measuring position (but not parity) is exactly sufficient
to reproduce classical statistics. The parity remains a coherent quantum
degree of freedom that cannot be read without disturbing the walk.

**Physical realisation:** Attenuated laser + SPAD array + photon counter.

---

## Comparison Table

| Property | Classical MC | Coherent Optical | Single-Photon QW |
|----------|-------------|-----------------|-----------------|
| α₊ formula | ½[1+cosᴴ(π/W)] | **Sharper** version | ½[1+cosᴴ(π/W)] |
| Transition W | Wₑ ≈ 2.46√H | Shifted left | Wₑ ≈ 2.46√H |
| Noise | O(1/√N) | Zero (deterministic) | O(1/√N) |
| Parity decoherence | N/A | None | At each row |
| Physical state | Bead position | Optical field | Photon Fock state |
| Build difficulty | Easy | Medium | Hard |

---

## Why the Coherent Version Differs

In the coherent model, amplitudes at different positions interfere at the
seam. The even-parity sector constructively interferes (the seam phase i
adds coherently), while the odd sector partially destructively interferes.

Mathematically: the coherent propagator is the matrix exponential of the
antiperiodic Laplacian, whereas the classical propagator is the probability
transfer matrix. They share the same eigenvectors but the coherent version
weights them differently (complex vs real amplitudes).

---

## Which Version Is "Right"?

All three are correct descriptions of different physical systems:

- **Classical:** bead/particle boards, coarse-grained quantum systems
- **Coherent:** laser interferometers, classical wave optics
- **Single-photon:** genuine quantum experiments, SPAD detection

For testing the topological formula, the classical and single-photon versions
both match theory exactly and are interchangeable. The coherent version
reveals additional structure (the topological sharpening of the transition)
that is experimentally accessible in the optical realisation.
