"""
collider_mini.py — Möbius Galton Board: Mini Möbius Collider
=============================================================
Models counter-propagating beams in a single twisted (Möbius) ring.

Based on:
  - Talman, R. (1995). "Möbius accelerators." Phys. Rev. Lett. 74(8), 1436.
  - US Patent 5,557,178A (Talman, 1996): Twisted-beam storage ring.

Key idea:
  - A standard collider uses two separate rings for counter-rotating beams.
  - A Möbius ring has a single beam pipe with a half-twist. Particles
    injected in one direction naturally encounter counter-propagating
    particles at the crossing point — one passage per half-loop.
  - The topological twist ensures the collision point is always at the
    same azimuthal location.

This script simulates:
  1. Two counter-propagating wave-packets in a 1D Möbius ring.
  2. Parity of each packet (polarization / spin) under the Möbius twist.
  3. Collision cross-section enhancement from topology.
  4. Comparison to a standard (cylinder) ring.

Usage:
    python collider_mini.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

K_STAR = 1.0 / (2.0 * np.log(2.0))


# ---------------------------------------------------------------------------
# Wave-packet class
# ---------------------------------------------------------------------------

class WavePacket:
    def __init__(self, N: int, x0: float, k0: float, sigma: float, parity: int = 0):
        """
        Gaussian wave-packet on a ring of N sites.

        Parameters
        ----------
        x0     : initial centre position (in sites)
        k0     : initial wave-vector (in units of 2π/N)
        sigma  : initial spatial width (sites)
        parity : initial ℤ₂ parity (0 or 1)
        """
        self.N      = N
        self.parity = parity
        x           = np.arange(N, dtype=float)
        envelope    = np.exp(-0.5 * ((x - x0) / sigma) ** 2)
        carrier     = np.exp(1j * 2 * np.pi * k0 * x / N)
        psi         = envelope * carrier
        self.psi    = psi / np.linalg.norm(psi)

    def step(self, direction: int, topology: str = "mobius"):
        """
        Propagate one step in given direction (+1 or -1).
        topology: 'cylinder' (periodic) or 'mobius' (antiperiodic at seam).
        """
        psi_new = np.zeros_like(self.psi)
        N = self.N
        split = 1.0 / np.sqrt(2)

        for x in range(N):
            amp = self.psi[x] * split
            xn  = x + direction

            if 0 <= xn < N:
                psi_new[xn] += amp
            else:
                if topology == "cylinder":
                    psi_new[xn % N] += amp
                else:  # mobius
                    psi_new[xn % N] += amp * np.exp(1j * np.pi)
                    self.parity = 1 - self.parity

        self.psi = psi_new

    def intensity(self) -> np.ndarray:
        return np.abs(self.psi) ** 2

    def overlap(self, other: "WavePacket") -> float:
        """Collision probability: |⟨ψ₁|ψ₂⟩|²"""
        return float(np.abs(np.vdot(self.psi, other.psi)) ** 2)


# ---------------------------------------------------------------------------
# Collider simulation
# ---------------------------------------------------------------------------

def run_collider(
    N: int = 64,
    N_steps: int = 128,
    topology: str = "mobius",
    sigma: float = 4.0,
) -> dict:
    """
    Run counter-propagating wave-packets for N_steps on a ring of N sites.

    Returns
    -------
    dict with:
        'steps'          : step indices
        'overlap'        : collision overlap at each step
        'parity_a'       : parity of beam A
        'parity_b'       : parity of beam B
        'intensity_a'    : intensity trace (N_steps, N)
        'intensity_b'    : intensity trace (N_steps, N)
    """
    # Beam A: moving right (+1), start at position 0
    # Beam B: moving left  (-1), start at position N//2
    beam_a = WavePacket(N, x0=N * 0.1,  k0= 2.0, sigma=sigma, parity=0)
    beam_b = WavePacket(N, x0=N * 0.6,  k0=-2.0, sigma=sigma, parity=0)

    steps       = list(range(N_steps))
    overlaps    = []
    parity_a    = []
    parity_b    = []
    intensity_a = []
    intensity_b = []

    for _ in steps:
        overlaps.append(beam_a.overlap(beam_b))
        parity_a.append(beam_a.parity)
        parity_b.append(beam_b.parity)
        intensity_a.append(beam_a.intensity())
        intensity_b.append(beam_b.intensity())

        beam_a.step(+1, topology)
        beam_b.step(-1, topology)

    return {
        "steps"       : np.array(steps),
        "overlap"     : np.array(overlaps),
        "parity_a"    : np.array(parity_a),
        "parity_b"    : np.array(parity_b),
        "intensity_a" : np.array(intensity_a),
        "intensity_b" : np.array(intensity_b),
    }


# ---------------------------------------------------------------------------
# Compare topologies
# ---------------------------------------------------------------------------

def compare_topologies(N: int = 64, N_steps: int = 128):
    print("\nMini Möbius Collider — Topology Comparison")
    print(f"  Ring size N={N}, steps={N_steps}")

    res_mob = run_collider(N, N_steps, topology="mobius")
    res_cyl = run_collider(N, N_steps, topology="cylinder")

    peak_mob = res_mob["overlap"].max()
    peak_cyl = res_cyl["overlap"].max()

    print(f"\n  Peak collision overlap:")
    print(f"    Möbius   : {peak_mob:.4f}")
    print(f"    Cylinder : {peak_cyl:.4f}")
    print(f"    Ratio    : {peak_mob / peak_cyl:.2f}x")

    print("\n  Parity evolution at peak overlap step:")
    peak_step = int(res_mob["overlap"].argmax())
    print(f"    Step {peak_step}: parity_A={res_mob['parity_a'][peak_step]}, "
          f"parity_B={res_mob['parity_b'][peak_step]}")

    return res_mob, res_cyl


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

def plot_results():
    N, N_steps = 64, 200
    res_mob, res_cyl = compare_topologies(N, N_steps)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Mini Möbius Collider vs Cylinder Ring", fontsize=13)

    steps = res_mob["steps"]

    # --- Overlap vs step ---
    ax = axes[0, 0]
    ax.plot(steps, res_mob["overlap"], "b-",  lw=2, label="Möbius")
    ax.plot(steps, res_cyl["overlap"], "r--", lw=2, label="Cylinder")
    ax.set_xlabel("Step")
    ax.set_ylabel("Collision overlap |⟨A|B⟩|²")
    ax.set_title("Collision probability vs step")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # --- Parity of beam A ---
    ax2 = axes[0, 1]
    ax2.step(steps, res_mob["parity_a"], "b-",  lw=1.5, label="Möbius parity_A", where="post")
    ax2.step(steps, res_cyl["parity_a"], "r--", lw=1.5, label="Cylinder parity_A", where="post")
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Parity (0=even, 1=odd)")
    ax2.set_title("Parity flips under Möbius twist")
    ax2.set_ylim(-0.1, 1.5)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # --- Intensity snapshots ---
    for ax_idx, (ax_row, topology, res, title) in enumerate([
        (axes[1, 0], "mobius",   res_mob, "Möbius: beam intensities at peak collision"),
        (axes[1, 1], "cylinder", res_cyl, "Cylinder: beam intensities at peak collision"),
    ]):
        peak_step = int(res["overlap"].argmax())
        x_vals    = np.arange(N)
        ax_row.fill_between(x_vals, res["intensity_a"][peak_step],
                            alpha=0.6, color="steelblue", label="Beam A")
        ax_row.fill_between(x_vals, res["intensity_b"][peak_step],
                            alpha=0.6, color="tomato",    label="Beam B")
        ax_row.set_xlabel("Position")
        ax_row.set_ylabel("Intensity")
        ax_row.set_title(f"{title} (step {peak_step})")
        ax_row.legend(fontsize=9)
        ax_row.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("collider_mini_results.png", dpi=150)
    plt.show()
    print("Figure saved to collider_mini_results.png")


if __name__ == "__main__":
    plot_results()
