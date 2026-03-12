# Möbius Galton Board

[![CI](https://github.com/MacMayo1993/MobiusGalton/actions/workflows/ci.yml/badge.svg)](https://github.com/MacMayo1993/MobiusGalton/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Paper: arXiv](https://img.shields.io/badge/paper-arXiv-red.svg)](paper/main.tex)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)

> **The first non-orientable Galton board.** Watch *k\** = 1/(2 ln 2) ≈ 0.7213 emerge from topology. Simulations, inverse solver, optical & quantum versions, and physical build plans.

---

## What Is This?

A classical Galton board whose **left and right edges are identified via a Möbius seam** — a half-twist that flips a ℤ₂ parity label on every crossing. This non-orientable topology produces a clean **phase transition** in the even-parity fraction α₊ at the information-theoretic constant:

```
k* = 1 / (2 ln 2) ≈ 0.7213
```

with critical width **Wₑ ≈ 2.46 √H**.

The analytic formula is exact:

```
α₊(W, H) = ½ [ 1 + cosᴴ(π/W) ]
```

and the **closed-form inverse** recovers topology from measurement:

```
W = π / arccos[ (2α₊ − 1)^(1/H) ]
```

---

## Repository Structure

```
/mobius-galton-board
├── README.md
├── LICENSE                    MIT
├── CITATION.cff               Academic citation
├── CONTRIBUTING.md
├── paper/                     Full LaTeX manuscript (Mayo 2026)
│   ├── main.tex
│   ├── sections/
│   ├── figures/
│   └── supplementary/
├── simulations/
│   ├── python/
│   │   ├── classical_mc.py          200k-particle Monte Carlo
│   │   ├── optical_coherent.py      Complex amplitude propagation
│   │   ├── single_photon.py         Quantum random walk
│   │   ├── inverse_solver.py        Exact W from α₊
│   │   ├── continuous_waveguide.py  Möbius strip waveguide model
│   │   ├── collider_mini.py         Counter-propagating beams
│   │   └── requirements.txt
│   ├── react/                       Interactive canvas demo
│   │   ├── src/
│   │   └── vite.config.ts
│   └── jupyter/
│       └── Möbius_Galton_Explorer.ipynb
├── physical_builds/
│   ├── mechanical/
│   ├── optical_lattice/
│   └── micro_mobius/
├── docs/
│   ├── theory.md
│   ├── inverse_formula.md
│   ├── optical_vs_quantum.md
│   └── collider_extension.md
├── assets/
│   └── images/
└── .github/workflows/ci.yml
```

---

## Quick Start

### Python Simulations

```bash
cd simulations/python
pip install -r requirements.txt

# Classical Monte Carlo (200k particles)
python classical_mc.py

# Single-photon quantum walk
python single_photon.py

# Coherent optical simulation
python optical_coherent.py

# Inverse solver: recover W from α₊
python inverse_solver.py

# Continuous Möbius waveguide
python continuous_waveguide.py

# Mini Möbius collider
python collider_mini.py
```

### Interactive React Demo

```bash
cd simulations/react
npm install
npm run dev
```

Open http://localhost:5173 in your browser. Use the sliders to control **W** (board width) and **H** (board height), switch between **Classical / Cylinder / Möbius** modes, and watch α₊ evolve in real time with the k* phase-transition line.

### Jupyter Notebook

```bash
cd simulations/jupyter
jupyter notebook "Möbius_Galton_Explorer.ipynb"
```

---

## Key Results

| H | Wₑ (theory) | W at α₊=k* (sim) | α₊ at W=Wₑ |
|---|-------------|-------------------|------------|
| 9  | 7.38  | 7–8   | 0.7218 |
| 16 | 9.84  | 9–10  | 0.7214 |
| 25 | 12.30 | 12–13 | 0.7213 |
| 36 | 14.76 | 14–15 | 0.7213 |

The critical width scales as **Wₑ ≈ 2.46 √H** and the transition always converges to **k\* = 1/(2 ln 2)**.

---

## Physical Implementations

Three prototype pathways are fully documented in `physical_builds/`:

1. **Mechanical** — 3D-printed Galton board with helical seam tubes and two-tone parity beads
2. **Optical Lattice** — Beam-splitter cube grid with half-wave plate at the Möbius seam (Thorlabs parts list included)
3. **Micro-Möbius Waveguide** — Inject a single photon at the midline of a physical twisted dielectric strip; topology provides the Berry-phase π flip naturally

---

## Paper

The full manuscript is in `paper/main.tex` (Overleaf-compatible). Compile with:

```bash
cd paper && pdflatex main.tex && pdflatex main.tex
```

**Title:** *The Möbius Galton Board and the Emergence of k\**
**Author:** M. Mayo, SeamAware Research (2026)

---

## Citation

```bibtex
@software{mayo2026mobius,
  author    = {Mayo, M.},
  title     = {Möbius Galton Board},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/MacMayo1993/MobiusGalton}
}
```

See also `CITATION.cff` for the machine-readable format.

---

## License

- **Code:** MIT (see `LICENSE`)
- **Paper and figures:** CC-BY 4.0

---

## Contributing

See `CONTRIBUTING.md`. Bug reports, physical-build photos, and experiment results are especially welcome.

---

*"From a half-twist in a Galton board, a universal constant emerges."*
