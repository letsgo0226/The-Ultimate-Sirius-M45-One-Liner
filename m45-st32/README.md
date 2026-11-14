# M45-ST/32 — SK-to-Tape Bridge

This stage makes the interface between **SK prefix expressions** and **finite tape symbols** explicit:

- Tape alphabet: `@ → 0`, `S → 1`, `K → 2`.
- Tape decoding validates prefix SK syntax.
- A deterministic Python interpreter applies leftmost-outermost SK reductions in bounded batches.
- Each batch yields a SHA-256-linked record and a trace that can be independently recomputed by the included replay function.
- A read-only GitHub Actions workflow executes tests and uploads a certificate artifact.

## Run

```sh
python3 -m unittest discover -s m45-st32 -p 'test_*.py'
python3 m45-st32/sk_tape.py --expression '@@@SKKS' --steps 30
```

Expected: `@@@SKKS → @@KS@KS → S`.

## Critical scope distinction

**This is NOT a fixed finite transition-table single-tape Turing machine that performs SK reduction.** ST32 is an SK interpreter with an explicit finite tape encoding. The ST28/ST30 fixed-transition-table unary successor machine remains separate.

A future ST33 would need to compile or implement SK parsing and reduction using a specified finite set of TM states and tape alphabet, and demonstrate step-by-step equivalence with this reference interpreter. That proof is **not** present here.

Certificates detect accidental alteration relative to the known program and trace; SHA-256 is not a signature. GitHub Actions artifacts expire. No automatic state commits, permanent hosting, or autonomous continuation are claimed.

## GitHub publication

This PR is stacked on ST31, itself stacked on ST30/ST29/ST28. Review and merge dependent PRs in order. The workflow is not live on the default branch until merged.
