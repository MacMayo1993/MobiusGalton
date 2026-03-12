"""
classical_mc.py — Möbius Galton Board: Classical Monte Carlo Simulation
========================================================================
Simulates N particles dropping through a Galton board with three boundary
conditions:
  - standard  : reflecting walls
  - cylinder  : periodic (left ↔ right, same parity)
  - mobius    : antiperiodic (left ↔ right with ℤ₂ parity flip)

Validates the analytic formula:
    α₊(W, H) = ½ [1 + cosᴴ(π/W)]

and locates the phase transition at k* = 1/(2 ln 2) ≈ 0.7213,
with critical width Wₑ ≈ 2.46 √H.

Usage:
    python classical_mc.py
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Literal

RNG = np.random.default_rng(42)

K_STAR = 1.0 / (2.0 * np.log(2.0))   # ≈ 0.7213


# ---------------------------------------------------------------------------
# Core simulation
# ---------------------------------------------------------------------------

def run_simulation(
    W: int,
    H: int,
    N: int = 200_000,
    mode: Literal["standard", "cylinder", "mobius"] = "mobius",
) -> tuple[float, np.ndarray, np.ndarray]:
    """
    Drop N particles through a W-wide, H-row Galton board.

    Returns
    -------
    alpha_plus : float
        Fraction of particles ending with even parity.
    positions : ndarray, shape (N,)
        Final x positions in [0, W-1].
    parities : ndarray, shape (N,), dtype int
        Final parities: 0 = even, 1 = odd.
    """
    positions = np.zeros(N, dtype=np.float64)
    parities  = np.zeros(N, dtype=np.int32)   # 0 = even, 1 = odd

    for _ in range(H):
        steps = RNG.integers(0, 2, size=N) * 2 - 1   # ±1
        positions += steps

        if mode == "standard":
            # Reflect at walls
            positions = np.where(positions < 0,      -positions,      positions)
            positions = np.where(positions >= W, 2*W - 2 - positions, positions)

        elif mode == "cylinder":
            # Wrap without parity change
            positions = positions % W

        elif mode == "mobius":
            # Wrap with parity flip on each crossing
            crossings = (positions // W).astype(np.int32)
            positions = positions % W
            parities  = (parities + np.abs(crossings)) % 2

    alpha_plus = float(np.mean(parities == 0))
    return alpha_plus, positions.astype(np.int32), parities


# ---------------------------------------------------------------------------
# Analytic formula
# ---------------------------------------------------------------------------

def analytic_alpha(W: float, H: int) -> float:
    """α₊(W, H) = ½ [1 + cosᴴ(π/W)]"""
    return 0.5 * (1.0 + np.cos(np.pi / W) ** H)


def critical_width(H: int) -> float:
    """Wₑ ≈ 2.46 √H  (from spectral gap condition α₊ = k*)"""
    return np.pi / np.arccos((2.0 * K_STAR - 1.0) ** (1.0 / H))


# ---------------------------------------------------------------------------
# Table scan over W values
# ---------------------------------------------------------------------------

def scan_widths(H: int = 25, W_range: range = range(8, 31), N: int = 200_000):
    print(f"\nMöbius Galton Board — Monte Carlo scan  (H={H}, N={N:,})")
    print(f"{'W':>4}  {'α₊ (sim)':>10}  {'α₊ (theory)':>12}  {'Δ':>8}  {'note':>6}")
    print("-" * 50)

    Wc = critical_width(H)

    sim_vals     = []
    theory_vals  = []
    W_vals       = list(W_range)

    for W in W_vals:
        a_sim, _, _ = run_simulation(W, H, N, mode="mobius")
        a_th        = analytic_alpha(W, H)
        sim_vals.append(a_sim)
        theory_vals.append(a_th)
        note = "<-- k*" if abs(a_th - K_STAR) < 0.005 else ""
        print(f"{W:>4}  {a_sim:>10.4f}  {a_th:>12.4f}  {a_sim - a_th:>+8.4f}  {note}")

    print(f"\nk*  = {K_STAR:.4f}")
    print(f"Wₑ  = {Wc:.3f}  (≈ 2.46 √{H} = {2.46*H**0.5:.3f})")
    return W_vals, sim_vals, theory_vals


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_results(H: int = 25, W_range: range = range(5, 35)):
    W_vals, sim_vals, theory_vals = scan_widths(H, W_range)

    W_fine  = np.linspace(W_range.start, W_range.stop, 300)
    a_fine  = [analytic_alpha(w, H) for w in W_fine]
    Wc      = critical_width(H)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(f"Möbius Galton Board  (H = {H})", fontsize=14)

    # --- Left: α₊ vs W ---
    ax = axes[0]
    ax.plot(W_fine,  a_fine,     "b-",  lw=2,   label="Analytic")
    ax.scatter(W_vals, sim_vals, c="red", zorder=5, label="Monte Carlo")
    ax.axhline(K_STAR, color="green", ls="--", lw=1.5, label=f"k* ≈ {K_STAR:.4f}")
    ax.axvline(Wc,     color="purple", ls=":",  lw=1.5, label=f"Wₑ ≈ {Wc:.2f}")
    ax.set_xlabel("Board width W")
    ax.set_ylabel("α₊  (even-parity fraction)")
    ax.set_title("Phase transition in α₊")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # --- Right: histogram of final parity distribution at W=Wc ---
    W_near = int(round(Wc))
    a_sim, positions, parities = run_simulation(W_near, H, N=200_000, mode="mobius")
    even_pos = positions[parities == 0]
    odd_pos  = positions[parities == 1]

    bins = np.arange(W_near + 1) - 0.5
    ax2 = axes[1]
    ax2.hist(even_pos, bins=bins, alpha=0.7, label=f"Even  (α₊={np.mean(parities==0):.3f})",
             color="steelblue", edgecolor="white")
    ax2.hist(odd_pos,  bins=bins, alpha=0.7, label="Odd",
             color="tomato",    edgecolor="white")
    ax2.set_xlabel("Final position")
    ax2.set_ylabel("Count")
    ax2.set_title(f"Parity histogram at W={W_near} ≈ Wₑ")
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("classical_mc_results.png", dpi=150)
    plt.show()
    print("\nFigure saved to classical_mc_results.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    plot_results(H=25, W_range=range(5, 35))
