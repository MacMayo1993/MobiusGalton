"""
optical_coherent.py — Möbius Galton Board: Coherent Optical Simulation
=======================================================================
Propagates complex probability amplitudes through a Galton board lattice.
At each peg, amplitude splits 50/50. At the Möbius seam crossing, the
amplitude picks up a phase factor of i (models a half-wave plate / π/2
phase shift), implementing the topological ℤ₂ parity flip in the optical
domain.

Even-parity amplitude dominates more strongly than in the classical case
due to constructive/destructive interference, shifting the phase boundary
leftward.

Usage:
    python optical_coherent.py
"""

import numpy as np
import matplotlib.pyplot as plt

K_STAR = 1.0 / (2.0 * np.log(2.0))


# ---------------------------------------------------------------------------
# Complex-amplitude propagation
# ---------------------------------------------------------------------------

def propagate_coherent(W: int, H: int) -> tuple[float, np.ndarray]:
    """
    Propagate a coherent state through a W×H Möbius Galton board.

    Initial state: uniform amplitude, even parity, at position 0.

    Returns
    -------
    alpha_plus : float
        Even-parity intensity fraction  Σ|ψ₊|² / (Σ|ψ₊|² + Σ|ψ₋|²)
    intensities : ndarray, shape (W, 2)
        Column 0: even-parity intensity at each final position.
        Column 1: odd-parity intensity at each final position.
    """
    # State: complex array of shape (W, 2)  — (position, parity)
    # parity 0 = even, parity 1 = odd
    psi = np.zeros((W, 2), dtype=complex)
    psi[0, 0] = 1.0          # Start at x=0, even parity

    split = 1.0 / np.sqrt(2)  # 50/50 beamsplitter amplitude

    for _ in range(H):
        psi_new = np.zeros_like(psi)
        for x in range(W):
            for p in range(2):
                amp = psi[x, p] * split

                # Step right
                xr = x + 1
                if xr < W:
                    psi_new[xr, p] += amp
                else:
                    # Möbius seam: wrap with phase i and parity flip
                    xr_wrapped = xr % W
                    psi_new[xr_wrapped, 1 - p] += amp * 1j

                # Step left
                xl = x - 1
                if xl >= 0:
                    psi_new[xl, p] += amp
                else:
                    # Möbius seam: wrap with phase i and parity flip
                    xl_wrapped = (xl + W) % W
                    psi_new[xl_wrapped, 1 - p] += amp * 1j

        psi = psi_new

    intensities = np.abs(psi) ** 2
    total_even = intensities[:, 0].sum()
    total_odd  = intensities[:, 1].sum()
    total      = total_even + total_odd
    alpha_plus = total_even / total if total > 0 else 0.5
    return float(alpha_plus), intensities


# ---------------------------------------------------------------------------
# Analytic (classical) baseline
# ---------------------------------------------------------------------------

def analytic_alpha(W: float, H: int) -> float:
    return 0.5 * (1.0 + np.cos(np.pi / W) ** H)


def critical_width(H: int) -> float:
    return np.pi / np.arccos((2.0 * K_STAR - 1.0) ** (1.0 / H))


# ---------------------------------------------------------------------------
# Scan and compare
# ---------------------------------------------------------------------------

def scan_and_compare(H: int = 20, W_range: range = range(4, 28)):
    print(f"\nCoherent Optical Möbius Board  (H={H})")
    print(f"{'W':>4}  {'α₊ (optical)':>14}  {'α₊ (classical)':>16}")
    print("-" * 40)

    W_vals, optical_vals, classical_vals = [], [], []

    for W in W_range:
        a_opt, _ = propagate_coherent(W, H)
        a_cls    = analytic_alpha(W, H)
        W_vals.append(W)
        optical_vals.append(a_opt)
        classical_vals.append(a_cls)
        print(f"{W:>4}  {a_opt:>14.4f}  {a_cls:>16.4f}")

    Wc = critical_width(H)
    print(f"\nClassical k* = {K_STAR:.4f},  Wₑ(classical) = {Wc:.2f}")
    return W_vals, optical_vals, classical_vals


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

def plot_results(H: int = 20):
    W_range = range(3, 28)
    W_vals, optical_vals, classical_vals = scan_and_compare(H, W_range)

    W_fine = np.linspace(3, 27, 400)
    cls_fine = [analytic_alpha(w, H) for w in W_fine]
    Wc = critical_width(H)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(f"Coherent Optical vs Classical Möbius Board  (H={H})", fontsize=13)

    ax = axes[0]
    ax.plot(W_fine, cls_fine,      "b-",  lw=2,   label="Classical (analytic)")
    ax.plot(W_vals, optical_vals,  "ro-", lw=1.5, label="Coherent optical", markersize=5)
    ax.axhline(K_STAR, color="green", ls="--", lw=1.5, label=f"k* ≈ {K_STAR:.4f}")
    ax.axvline(Wc,     color="purple", ls=":",  lw=1.5, label=f"Wₑ(classical) ≈ {Wc:.1f}")
    ax.set_xlabel("Board width W")
    ax.set_ylabel("α₊  (even-parity fraction)")
    ax.set_title("Phase transition comparison")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Intensity map at W ≈ Wc
    W_near = max(3, int(round(Wc)))
    _, intensities = propagate_coherent(W_near, H)

    ax2 = axes[1]
    x_vals = np.arange(W_near)
    ax2.bar(x_vals - 0.2, intensities[:, 0], width=0.35,
            label="Even parity", color="steelblue", alpha=0.85)
    ax2.bar(x_vals + 0.2, intensities[:, 1], width=0.35,
            label="Odd parity",  color="tomato",    alpha=0.85)
    ax2.set_xlabel("Position")
    ax2.set_ylabel("Intensity |ψ|²")
    ax2.set_title(f"Final intensity distribution  (W={W_near})")
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("optical_coherent_results.png", dpi=150)
    plt.show()
    print("Figure saved to optical_coherent_results.png")


if __name__ == "__main__":
    plot_results(H=20)
