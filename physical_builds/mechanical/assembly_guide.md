# Mechanical Möbius Galton Board — Assembly Guide

## Overview

A 3D-printed Galton board (W=14, H=15 recommended for visibility) with helical
seam tubes connecting the left and right boundary exits. Two-tone parity beads
(blue = even, red = odd) track ℤ₂ parity visually. Measure α₊ by counting
bead colours in each collection bin.

---

## Bill of Materials

| # | Item | Qty | Source | Est. Cost |
|---|------|-----|--------|-----------|
| 1 | PLA/PETG filament (white) | 1 kg | Amazon/local | $20 |
| 2 | 8mm steel rod (pegs), 15 cm lengths | 2× | Hardware store | $8 |
| 3 | 6mm OD acrylic tube (seam conduit) | 2× 30 cm | Amazon | $10 |
| 4 | Two-tone beads: blue 10mm (even) | 500 | Amazon | $12 |
| 5 | Two-tone beads: red 10mm (odd) | 500 | Amazon | $12 |
| 6 | M3 hex nuts + bolts (assembly) | 30 | Hardware | $5 |
| 7 | Clear acrylic sheet 3mm (front cover) | 1 | Amazon | $15 |
| 8 | Spring steel clips (bead storage) | 4 | Hardware | $4 |
| **Total** | | | | **~$86** |

---

## STL Files

All STL files are in the `STL/` folder:

| File | Description |
|------|-------------|
| `board_frame.stl` | Main board frame (W=14 columns, H=15 rows) |
| `peg_row_even.stl` | Staggered peg row for even row index |
| `peg_row_odd.stl` | Staggered peg row for odd row index |
| `seam_tube_left.stl` | Left-boundary helical conduit |
| `seam_tube_right.stl` | Right-boundary helical conduit (mirror) |
| `bin_collector.stl` | Bottom collection bin array (14 slots) |
| `funnel_top.stl` | Ball-drop funnel for single-ball input |
| `parity_gate.stl` | Parity-labelling gate (auto-paints even on entry) |

Print settings: 0.2 mm layer height, 20% infill, supports for seam tubes.

---

## Assembly Steps

### Step 1: Print all STL files
Print `board_frame.stl` first — this is the largest print (~6 hrs at 0.2 mm).
Print peg rows as a batch (30 total rows). Use white or light-grey filament.

### Step 2: Install pegs
Press 8 mm steel rod sections into peg holes. Each row has W+1 = 15 pegs
in alternating positions. Rows alternate between `peg_row_even.stl` and
`peg_row_odd.stl` geometries.

### Step 3: Install seam tubes
The critical step. Insert `seam_tube_left.stl` into the left boundary exit
slots and `seam_tube_right.stl` into the right boundary. The tubes are
helical — they cross in the middle of the board, creating the Möbius
identification. A ball exiting right re-enters left and vice versa.

**Parity mechanism:** Place a half-twist collar at the midpoint of each
seam tube. The twist physically flips the bead's "top" face, which carries
the parity colour label — automating the ℤ₂ parity flip.

### Step 4: Attach front cover
Secure the 3mm acrylic sheet to the front face of the board frame using
M3 bolts. This keeps balls on the correct row during descent.

### Step 5: Install collection bins
Press `bin_collector.stl` into the bottom slot. Label bins 0–13 (left to right).

### Step 6: Parity gate
Install `parity_gate.stl` at the top funnel. This device ensures every ball
entering the board starts as **even parity** (blue face up). No manual
labelling required.

---

## Calibration and Measurement

1. Load 100 beads through the funnel (all starting even/blue).
2. After all beads settle, count blue (even) beads across all bins → N_even.
3. Total dropped = N. Compute α₊ = N_even / N.
4. Compare to theory: α₊(14, 15) = ½[1 + cos(π/14)^15] ≈ 0.763.
5. Use the inverse formula to recover W:
   ```
   W_recovered = π / arccos[(2α₊ − 1)^(1/H)]
   ```
   Should return ≈ 14.0 for a well-aligned board.

**Repeat with 500+ beads** for statistical accuracy within ±0.01 of theory.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Beads jam in seam tube | Tube ID too tight | Drill to 10.5 mm ID |
| Wrong parity fraction | Seam tube twisted wrong direction | Flip one tube |
| Beads skip pegs | Peg spacing too wide | Reduce peg pitch in CAD |
| Bead clusters at walls | Reflecting instead of seam | Check tube connections |
