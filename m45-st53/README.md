# M45-ST/53 — Observational Type Transformation Algebra

This prototype formalizes a limited algebra of **unitary-conjugation transformations** on real-qubit Bloch coordinates `(x,z)`, with `x²+z² <= 1`. All arithmetic uses exact Python rational fractions.

- Hadamard conjugation H maps `(x,z) -> (z,x)`.
- Pauli-Z conjugation Z maps `(x,z) -> (-x,z)`.
- Operators compose in written left-to-right application order. `HH = ZZ = identity`, and `(HZ)^4 = identity` at the density-operator level.
- For each resulting X or Z measurement, the program computes the **corresponding signed measurement axis in the input frame**, and checks Born-probability covariance.

```sh
python3 -m unittest discover -s m45-st53 -p 'test_*.py'
python3 m45-st53/transform_algebra.py --x 3/5 --z 4/5 --word HZ
```

**Crucial distinction:** Applying a unitary to a physical state while keeping the detector fixed is not the same as simply changing the detector. Covariance means that transforming the state and consistently transforming the observable gives matching predictions. This is a finite mathematical representation of known quantum mechanics, not evidence that observer choices change physical laws.

The H/Z generated group here is finite and does not describe arbitrary qubit rotations, environment-induced decoherence, or an actual astrophysical instrument. No particles are physically prepared, no collapse is asserted, and no physical universe is controlled. Read-only CI; draft stacked on ST52.
