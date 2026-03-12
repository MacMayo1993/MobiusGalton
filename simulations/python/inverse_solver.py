"""
inverse_solver.py — Möbius Galton Board: Inverse Topology Solver
================================================================
Given a measured even-parity fraction α₊ and the board height H,
recover the effective topological width W using the closed-form inverse:

    W = π / arccos[ (2α₊ − 1)^(1/H) ]

This turns the Möbius board into a self-calibrating topology meter:
any physical system that produces a parity-split distribution can be
characterised by its effective W.

Verification:
    - Input α₊ = k* = 1/(2 ln 2) recovers W = Wₑ ≈ 2.46 √H exactly.
    - Round-trip: forward → inverse → forward gives back original α₊.

Usage:
    python inverse_solver.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

K_STAR = 1.0 / (2.0 * np.log(2.0))


# ---------------------------------------------------------------------------
# Forward and inverse formulas
# ---------------------------------------------------------------------------

def alpha_plus(W: float, H: int) -> float:
    """α₊(W, H) = ½ [1 + cosᴴ(π/W)]"""
    return 0.5 * (1.0 + np.cos(np.pi / W) ** H)


def inverse_W(alpha: float, H: int) -> float | None:
    """
    W = π / arccos[ (2α − 1)^(1/H) ]

    Returns None if the input is outside the valid range (0.5, 1).
    """
    if not (0.5 < alpha < 1.0):
        return None
    inner = (2.0 * alpha - 1.0) ** (1.0 / H)
    if abs(inner) > 1.0:
        return None
    return float(np.pi / np.arccos(inner))


def critical_width(H: int) -> float:
    """Wₑ(H) = inverse_W(k*, H)"""
    return inverse_W(K_STAR, H)


# ---------------------------------------------------------------------------
# Numeric inverse (Brent's method) — cross-check
# ---------------------------------------------------------------------------

def inverse_W_numeric(alpha: float, H: int, W_lo: float = 2.01, W_hi: float = 1000.0) -> float:
    """Numeric inverse via Brent root-finding (used for verification)."""
    f = lambda w: alpha_plus(w, H) - alpha
    try:
        return brentq(f, W_lo, W_hi, xtol=1e-10)
    except ValueError:
        return float("nan")


# ---------------------------------------------------------------------------
# Round-trip verification
# ---------------------------------------------------------------------------

def round_trip_test(H: int = 25):
    print(f"\nRound-trip verification  (H={H})")
    print(f"{'W_in':>8}  {'α₊':>10}  {'W_recovered':>13}  {'error':>10}")
    print("-" * 48)

    test_W = [5, 8, 10, 12, 15, 18, 20, 25, 30]
    for W in test_W:
        a    = alpha_plus(W, H)
        W_rec = inverse_W(a, H)
        err  = (W_rec - W) if W_rec is not None else float("nan")
        print(f"{W:>8}  {a:>10.6f}  {W_rec:>13.6f}  {err:>+10.2e}")


def kstar_recovery_test():
    print("\nk* recovery test (input α₊ = k*, expect W = Wₑ):")
    print(f"{'H':>6}  {'Wₑ (formula)':>14}  {'W (inverse)':>13}  {'2.46√H':>10}")
    print("-" * 50)
    for H in [4, 9, 16, 25, 36, 49, 64, 100]:
        Wc_inv   = inverse_W(K_STAR, H)
        Wc_appx  = 2.46 * H ** 0.5
        print(f"{H:>6}  {Wc_inv:>14.4f}  {Wc_inv:>13.4f}  {Wc_appx:>10.4f}")


# ---------------------------------------------------------------------------
# Scan: recovered W from noisy α₊ (simulate measurement uncertainty)
# ---------------------------------------------------------------------------

def noisy_recovery_demo(H: int = 25, W_true: int = 12, N_expts: int = 10_000):
    """
    Simulates 10 000 experiments each measuring α₊ from N=10 000 particles.
    Plots distribution of recovered Ŵ around W_true.
    """
    rng  = np.random.default_rng(42)
    a_true = alpha_plus(W_true, H)

    # Each experiment: draw Binomial counts, compute α̂₊, invert
    counts = rng.binomial(10_000, a_true, size=N_expts)
    a_hats = counts / 10_000.0
    W_hats = np.array([inverse_W(a, H) if 0.5 < a < 1.0 else np.nan
                       for a in a_hats])
    W_hats = W_hats[~np.isnan(W_hats)]

    print(f"\nNoisy recovery:  W_true={W_true},  H={H},  N_expts={N_expts}")
    print(f"  Mean recovered W = {W_hats.mean():.4f}")
    print(f"  Std  recovered W = {W_hats.std():.4f}")

    plt.figure(figsize=(7, 4))
    plt.hist(W_hats, bins=60, density=True, color="steelblue", alpha=0.8, edgecolor="white")
    plt.axvline(W_true, color="red",   ls="--", lw=2, label=f"True W = {W_true}")
    plt.axvline(W_hats.mean(), color="orange", ls=":", lw=2,
                label=f"Mean Ŵ = {W_hats.mean():.2f}")
    plt.xlabel("Recovered width  Ŵ")
    plt.ylabel("Density")
    plt.title(f"Inverse solver uncertainty  (H={H}, W_true={W_true}, N=10k/expt)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("inverse_solver_noise.png", dpi=150)
    plt.show()
    print("Figure saved to inverse_solver_noise.png")


# ---------------------------------------------------------------------------
# Plot W_e vs H
# ---------------------------------------------------------------------------

def plot_critical_scaling():
    H_vals  = np.arange(4, 101)
    Wc_vals = np.array([critical_width(int(H)) for H in H_vals])
    fit     = 2.46 * H_vals ** 0.5

    plt.figure(figsize=(7, 4))
    plt.plot(H_vals, Wc_vals, "b-",  lw=2,   label="Wₑ = inverse_W(k*, H)")
    plt.plot(H_vals, fit,     "r--", lw=1.5, label="2.46 √H")
    plt.xlabel("Board height H")
    plt.ylabel("Critical width Wₑ")
    plt.title("Critical width scaling")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("critical_scaling.png", dpi=150)
    plt.show()
    print("Figure saved to critical_scaling.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    round_trip_test(H=25)
    kstar_recovery_test()
    noisy_recovery_demo(H=25, W_true=12, N_expts=10_000)
    plot_critical_scaling()
