"""
continuous_waveguide.py — Möbius Galton Board: Continuous Waveguide Model
==========================================================================
Models a photon propagating on a physical Möbius-strip dielectric waveguide.

Key idea:
  - The strip has length L and width d. It is twisted by π (half-turn).
  - A photon injected at the midline (the "halfway cut" of the strip)
    travels along the waveguide and acquires a geometric (Berry) phase of π
    on completing one loop — the non-orientable topology provides the
    natural polarization flip.
  - The photon interferes with itself across the non-orientable surface.

We model the waveguide as a discrete lattice of length N_steps along the
strip, with transverse width W discretised into W_bins slots. The twist
introduces antiperiodic boundary conditions in the transverse direction at
the seam (halfway along the loop), exactly mirroring the discrete Möbius
Galton board.

Observables:
  - Polarization parity fraction α₊ as a function of propagation distance
  - Transverse intensity profile at each distance
  - Berry phase accumulation

Usage:
    python continuous_waveguide.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

K_STAR = 1.0 / (2.0 * np.log(2.0))


# ---------------------------------------------------------------------------
# Continuous Möbius waveguide propagation
# ---------------------------------------------------------------------------

def propagate_waveguide(
    W: int = 12,
    N_steps: int = 50,
    seam_at: int | None = None,
    injection_pos: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Propagate a photon along a Möbius-strip waveguide.

    Parameters
    ----------
    W            : transverse width (number of bins)
    N_steps      : longitudinal propagation steps (one full loop)
    seam_at      : step index where the Möbius seam occurs (default: N_steps//2)
    injection_pos: transverse injection position (default: midline W//2)

    Returns
    -------
    alpha_plus_trace : ndarray shape (N_steps+1,)
        Even-parity intensity fraction at each step.
    psi_trace : ndarray shape (N_steps+1, W, 2)
        Full complex amplitude at each step.
    """
    if seam_at is None:
        seam_at = N_steps // 2
    if injection_pos is None:
        injection_pos = W // 2

    psi = np.zeros((W, 2), dtype=complex)
    psi[injection_pos, 0] = 1.0   # even parity, midline injection

    split = 1.0 / np.sqrt(2)

    psi_trace         = [psi.copy()]
    alpha_plus_trace  = [_alpha(psi)]

    for step in range(N_steps):
        psi_new = np.zeros_like(psi)
        at_seam = (step == seam_at)

        for x in range(W):
            for p in range(2):
                amp = psi[x, p] * split

                # Right step
                xr = x + 1
                if xr < W:
                    psi_new[xr, p] += amp
                else:
                    if at_seam:
                        # Möbius: parity flip + Berry phase
                        psi_new[xr % W, 1 - p] += amp * np.exp(1j * np.pi)
                    else:
                        # Reflecting boundary (transverse edges)
                        psi_new[W - 1, p] += amp

                # Left step
                xl = x - 1
                if xl >= 0:
                    psi_new[xl, p] += amp
                else:
                    if at_seam:
                        psi_new[(xl + W) % W, 1 - p] += amp * np.exp(1j * np.pi)
                    else:
                        psi_new[0, p] += amp

        psi = psi_new
        psi_trace.append(psi.copy())
        alpha_plus_trace.append(_alpha(psi))

    return np.array(alpha_plus_trace), np.array(psi_trace)


def _alpha(psi: np.ndarray) -> float:
    i_even = np.abs(psi[:, 0]) ** 2
    i_odd  = np.abs(psi[:, 1]) ** 2
    total  = i_even.sum() + i_odd.sum()
    return float(i_even.sum() / total) if total > 0 else 0.5


# ---------------------------------------------------------------------------
# Berry phase demonstration
# ---------------------------------------------------------------------------

def berry_phase_demo(W: int = 12, N_steps: int = 100):
    """Show how α₊ evolves as the photon completes multiple loops."""
    print(f"\nBerry phase / multi-loop propagation  (W={W})")
    print(f"{'Loop':>6}  {'Step':>6}  {'α₊':>10}")
    print("-" * 28)

    traces = []
    for n_loops in range(1, 5):
        a_trace, _ = propagate_waveguide(W=W, N_steps=N_steps * n_loops)
        traces.append(a_trace)
        print(f"{n_loops:>6}  {N_steps * n_loops:>6}  {a_trace[-1]:>10.4f}")

    return traces


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_results():
    W, N = 12, 50

    alpha_trace, psi_trace = propagate_waveguide(W=W, N_steps=N)
    seam_step = N // 2

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"Continuous Möbius Waveguide  (W={W}, N_steps={N})", fontsize=13)

    # --- α₊ along propagation ---
    ax = axes[0]
    steps = np.arange(len(alpha_trace))
    ax.plot(steps, alpha_trace, "b-", lw=2)
    ax.axvline(seam_step, color="red",   ls="--", lw=1.5, label="Möbius seam")
    ax.axhline(K_STAR,    color="green", ls=":",  lw=1.5, label=f"k* ≈ {K_STAR:.4f}")
    ax.axhline(0.5,       color="gray",  ls=":",  lw=1.0, label="0.5")
    ax.set_xlabel("Propagation step")
    ax.set_ylabel("α₊")
    ax.set_title("Even-parity fraction along strip")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # --- Transverse intensity profile (even parity) at final step ---
    ax2 = axes[1]
    final_even = np.abs(psi_trace[-1, :, 0]) ** 2
    final_odd  = np.abs(psi_trace[-1, :, 1]) ** 2
    x_vals = np.arange(W)
    ax2.bar(x_vals - 0.2, final_even, width=0.35, color="steelblue", alpha=0.85,
            label=f"Even  α₊={alpha_trace[-1]:.3f}")
    ax2.bar(x_vals + 0.2, final_odd,  width=0.35, color="tomato",    alpha=0.85,
            label="Odd")
    ax2.set_xlabel("Transverse position")
    ax2.set_ylabel("Intensity |ψ|²")
    ax2.set_title("Final transverse distribution")
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    # --- Propagation map (even parity intensity vs step and position) ---
    ax3 = axes[2]
    even_map = np.abs(psi_trace[:, :, 0]) ** 2   # shape (N+1, W)
    im = ax3.imshow(even_map.T, aspect="auto", origin="lower",
                    extent=[0, N, 0, W - 1], cmap="viridis")
    ax3.axvline(seam_step, color="red", ls="--", lw=1.5, label="seam")
    ax3.set_xlabel("Propagation step")
    ax3.set_ylabel("Transverse position")
    ax3.set_title("Even-parity intensity map")
    ax3.legend(fontsize=9)
    plt.colorbar(im, ax=ax3, fraction=0.04)

    plt.tight_layout()
    plt.savefig("continuous_waveguide_results.png", dpi=150)
    plt.show()
    print("Figure saved to continuous_waveguide_results.png")

    # Multi-loop
    berry_phase_demo(W=W, N_steps=50)


if __name__ == "__main__":
    plot_results()
