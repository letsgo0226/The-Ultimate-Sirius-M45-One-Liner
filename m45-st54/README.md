# M45-ST/54 — Micro–Macro Operator Correspondence

This stage combines the exact-rational single-qubit H/Z transformation algebra of ST53 with the independent-qubit binomial coarse-graining of ST50.

For an identical product state of N qubits and a projective measurement along an axis A, let `C_N(rho,A)` be the binomial distribution of the number of plus outcomes. For U from the finite H/Z operator family:

`C_N(U rho U†, A) = C_N(rho, U† A U)`.

This is the **commuting diagram** being checked. It requires transforming the measurement axis consistently: H maps a final Z measurement to an initial X measurement, while Z maps a final X measurement to an initial minus-X measurement. A minus-axis measurement reverses the plus/minus labels; it does not violate covariance.

Run:
```sh
python3 -m unittest discover -s m45-st54 -p 'test_*.py'
python3 m45-st54/correspondence.py --n 32 --x 3/5 --z 4/5 --word HZ
```

Exact fractions are used for the qubit Bloch coordinates and Born probabilities; ST50's binomial distribution is floating-point and checked to tolerance 1e-12. The model assumes independent, identically prepared qubits, local identical unitary transformations, and X/Z projective measurements. It does **not** prove the same relation for interacting or entangled many-body systems, arbitrary coarse-graining, or objective collapse.

No telescope or particle detector is connected. GitHub Actions only runs bounded read-only tests. This is a mathematical correspondence, not evidence that the macro cosmos is literally hardware or the micro cosmos software.
