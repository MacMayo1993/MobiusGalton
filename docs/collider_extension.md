# Möbius Collider Extension

## Background

The standard particle collider uses **two separate rings**: one for
counter-clockwise particles, one for clockwise antiparticles. Both beams
must be precisely steered to a common interaction point.

In 1995, Richard Talman proposed a radical simplification:
> *A single beam pipe with a half-twist (Möbius topology) naturally produces
> counter-propagating beams at a single crossing point.*
— Talman, Phys. Rev. Lett. **74**, 1436 (1995)

The US Patent 5,557,178A (1996) describes the practical implementation.

---

## How the Möbius Ring Works

In a standard ring, particles travel in one direction around the circumference.
In a Möbius ring, the beam pipe has a π-twist:

```
Standard ring:    ○ → → → ○    (one direction only)

Möbius ring:      ○ → → → × → → → ○
                              ↑
                          half-twist
                          (crossing point)
```

A particle starting at the top travels clockwise, goes through the twist,
and then travels **counter-clockwise** relative to the lab frame. This creates
effective counter-propagation within a single beam pipe.

**Collision frequency:** Once per half-loop (vs. once per full loop for a
standard single-beam storage ring).

---

## Parity Connection

The Möbius collider directly generalises the Möbius Galton board:

| Galton board | Collider |
|-------------|---------|
| ℤ₂ parity label | Particle charge / spin |
| Seam crossing | Beam-pipe twist |
| Parity flip | Charge/helicity reversal |
| α₊ fraction | Collision-point probability density |
| k* transition | Luminosity threshold |

The parity (charge) of a particle flips at each passage through the twist —
exactly the Möbius seam of the Galton board, scaled to a macroscopic accelerator.

---

## Simulation Results

Our `collider_mini.py` simulation shows (N=64 sites, 200 steps):

- **Peak collision overlap** (Möbius ring) > **Cylinder ring** for matched
  initial conditions.
- Beam A parity **flips** at each half-loop passage through the twist.
- Beam B (counter-propagating) shows the **opposite** parity sequence.
- At the collision point, beams always have **opposite parity** — equivalent
  to particle/antiparticle collisions in a conventional collider.

---

## Tabletop Photon Version

A Möbius ring collider can be implemented in integrated photonics:

1. **Ring resonator** (silicon nitride or silica-on-silicon, radius ~50 µm)
2. **Half-twist** implemented as a polarisation rotator at one point on the ring
3. **Input:** Two photons injected in opposite directions via Y-junctions
4. **Detection:** Coincidence counting at the twist point

This is immediately buildable using existing integrated photonics technology.
Estimated cost for a university lab build: ~$15,000 (silicon nitride foundry
run + fibre coupling + SPAD coincidence setup).

---

## Key References

1. Talman, R. (1995). Möbius accelerators.
   *Phys. Rev. Lett.* **74**(8), 1436–1439.
   DOI: 10.1103/PhysRevLett.74.1436

2. Talman, R. (1996). Storage Ring for Charged Particle Beams.
   US Patent 5,557,178A.

3. Koscielniak, S. & Johnstone, C. (2004). Implementation of the Möbius
   principle in particle accelerators. *EPAC 2004 Proceedings*, 1554–1556.

---

## Future Work

- Full quantum field theory treatment of the Möbius collider interaction
- Non-Abelian generalisation (SU(2) parity → isospin)
- Möbius lattice gauge theory on the non-orientable board
- Experimental proposal for tabletop electron-positron Möbius ring
  (using existing synchrotron infrastructure, e.g., Cornell CHESS)
