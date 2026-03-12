# Optical Lattice Möbius Galton Board — Alignment Guide

## Overview

A 4×4 grid (W=4, H=4 recommended for first build) of 50:50 beamsplitter cubes
with a half-wave plate (HWP) at each Möbius seam boundary. Photons (780 nm)
enter from the top centre. Polarisation encodes parity: H-polarisation = even,
V-polarisation = odd. The HWP at the seam rotates polarisation by 90° on
seam crossing, implementing the ℤ₂ parity flip.

---

## Architecture

```
        INPUT (780 nm, H-pol = even parity)
              │
         [Collimator]
              │
    ┌─────────┴─────────┐
    │  Row 0: 4 BS cubes │
    └─────┬───────┬──────┘
         ...     ...
   [HWP at left edge]   [HWP at right edge]
         │                   │
    (parity flip)       (parity flip)
         │                   │
    ┌────┴───────────────┬───┘
    │  Row 3: 4 BS cubes │
    └────────────────────┘
              │
    [PBS — split H/V polarisation]
    H-pol → even detector (SPAD 1)
    V-pol → odd  detector (SPAD 2)
```

---

## Alignment Steps

### Step 1: Breadboard layout
Mount 16 BS cubes on the breadboard in a 4×4 grid with 50 mm pitch.
Use cage rods to constrain the cubes to a common optical axis.

### Step 2: Input beam alignment
Connect the 780 nm fibre source to the collimator. Adjust for a 3 mm
beam diameter. Check polarisation: should be H (horizontal).

### Step 3: Seam HWP installation
At each left and right boundary slot, install a WPH05M-780 half-wave plate
at 45° fast-axis orientation. This rotates H→V and V→H (i.e., even↔odd).

**Critical:** Both seam HWPs must have the same fast-axis orientation.
Use a polarimeter to confirm H→V rotation. An error of even 2° introduces
a measurable systematic in α₊.

### Step 4: Output PBS alignment
Place a PBS cube (PBS101) after the final row. The H transmission port
feeds SPAD 1 (even counter); the V reflection port feeds SPAD 2 (odd counter).

### Step 5: Baseline measurement (cylinder mode)
Remove both seam HWPs. Connect SPADs to HydraHarp 400. For a cylinder
board (no parity flip), theory predicts α₊ → 0.5 as H increases. Confirm
within ±0.02. This validates the beamsplitter grid alignment.

### Step 6: Möbius mode measurement
Reinstall seam HWPs. Measure α₊ for H=4. Theory: α₊(4, 4) = ½[1 + cos(π/4)^4]
= ½[1 + (√2/2)^4] = ½[1 + 0.25] = 0.625. Compare to SPAD count ratio.

---

## Computing α₊ from SPAD Counts

```
N_even = counts on SPAD 1 in integration window T
N_odd  = counts on SPAD 2 in integration window T
α₊     = N_even / (N_even + N_odd)
```

Then use the inverse formula to recover W:
```
W_recovered = π / arccos[(2α₊ − 1)^(1/H)]
```

For a 4×4 board, expect W_recovered ≈ 4.0 ± 0.3.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| α₊ ≈ 0.5 in Möbius mode | HWP not in beam path | Re-check seam HWP position |
| α₊ > 0.9 | Only one seam active | Check both left and right HWPs |
| Large oscillation in counts | Etalon effects in BS cube | Tilt BS cubes ±1° |
| α₊ doesn't match theory | Wrong HWP fast-axis angle | Re-measure with polarimeter |
