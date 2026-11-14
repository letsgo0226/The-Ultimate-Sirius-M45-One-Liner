# M45-ST/62 — Generalized Quantum Reference Frames

This prototype extends the ST61 real Bloch disk to **all three Bloch coordinates** and complex Hermitian 2×2 density matrices. It implements arbitrary axis-angle **SU(2)** rotations using only Python standard-library complex arithmetic.

For a Bloch vector r with |r|≤1, the density operator is `rho=(I+r·sigma)/2`. A projective measurement along a unit axis a uses `P_a=(I+a·sigma)/2`. Under the **passive simultaneous frame change** `rho'=U rho U†`, `P_a'=U P_a U†`, the Born probability is invariant:

`Tr(rho' P_a') = Tr(rho P_a)`.

The code reports both complex matrices (each entry as [real,imag]), the transported state, Born probabilities, purity `Tr(rho²)`, determinant, and maximum floating-point invariant error. Tests include Y-axis complex coherence, pure/mixed states, varied SU(2) axes and angles, and an explicit counterexample showing that changing the measurement without transporting the state need not preserve probabilities.

```sh
python3 -m unittest discover -s m45-st62 -p 'test_*.py'
python3 m45-st62/quantum_frames.py --bloch 0.3 0.4 0.5 --rotation-axis 1 2 3 --angle 1
```

**Scientific limits:** SU(2) basis/frame covariance is **not** a construction of quantum reference frames in the technical sense of reference frames that are themselves quantum systems; nor is it Lorentz covariance or a general relativity result. It does not equate individual stochastic outcomes, prove observer-independent ontology, solve the measurement problem, or implement physical laboratory measurements. Floating-point comparisons use tolerance 1e-10. Read-only CI.
