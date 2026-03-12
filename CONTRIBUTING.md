# Contributing to Möbius Galton Board

Thank you for your interest in contributing!

## Ways to Contribute

- **Bug reports** — Open a GitHub issue with reproduction steps
- **Physical build photos** — Share your mechanical or optical prototype in an issue; we will add it to the gallery
- **Experimental results** — If you have measured α₊ on a real board, open a PR to add your data to `physical_builds/`
- **Simulation improvements** — New boundary conditions, biased walks, 2D lattice versions
- **Documentation** — Corrections, clarifications, translations

## Development Setup

```bash
git clone https://github.com/MacMayo1993/MobiusGalton.git
cd MobiusGalton

# Python
cd simulations/python
pip install -r requirements.txt

# React
cd ../react
npm install
```

## Pull Request Guidelines

1. Fork the repo and create a branch from `main`
2. Write clear commit messages
3. For Python changes, ensure all scripts still run without error
4. For React changes, run `npm run build` and confirm no TypeScript errors
5. Reference any relevant issue number in your PR description

## Code Style

- Python: PEP 8, type hints on public functions
- TypeScript: standard strict mode
- Commit messages: imperative mood, ≤ 72 characters

## Academic Use

If this code contributes to a publication, please cite the repo and the original paper (see `CITATION.cff`). We encourage open replication of all results.

## License

By contributing you agree that your contributions will be licensed under the MIT License.
