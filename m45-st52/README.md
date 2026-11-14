# M45-ST/52 — Observational Equivalence Classes

This stage studies the equivalence relation `rho ~_C sigma` iff the two states produce **the same Born probability distribution under measurement context C**. This is a precise, context-relative notion of indistinguishability, not physical identity.

For a restricted family of real-valued qubit density matrices
`rho(p,c)=[[p,c],[c,1-p]]`, with rational p,c and `0 <= c^2 <= p(1-p)`:
- Z-plus probability is `p`.
- X-plus probability is `1/2+c`.
- Joint XZ data are the ordered pair `(p,1/2+c)`.

The program enumerates a bounded rational grid (denominator 1..32) using exact `fractions.Fraction`, partitions it into equivalence classes for Z, X and XZ, and outputs reproducible JSON.

```sh
python3 -m unittest discover -s m45-st52 -p 'test_*.py'
python3 m45-st52/equivalence.py --denominator 4
```

**Key point:** Two states with the same p but different c are indistinguishable by Z measurements, yet can be distinguished by X measurements. Adding measurement contexts refines equivalence classes. XZ is informationally complete **only within this restricted real-coherence family**; it is not complete tomography of arbitrary complex qubit density matrices (Y is needed for the imaginary coherence component).

The grid is an illustrative model, not a physical observation or evidence that the cosmos is computational software. Read-only CI. No persistent state writes or instruments.
