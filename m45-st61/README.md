# M45-ST/61 — Observer-Independent Invariants

This stage tests what remains invariant when an observer changes the *description frame* of a real qubit and transports the measurement axis along with it.

Use the restricted Bloch state `rho=(I+x sigma_X+z sigma_Z)/2`, with rational `x²+z²<=1`. Frame words built from H and Z act by exact signed-permutation matrices on `(x,z)`. For `r'=Ur` and `a'=Ua`, the Born probability `P(+|r,a)=(1+r·a)/2` is unchanged because `r'·a'=r·a`.

The exact invariants are trace `1`, purity `(1+x²+z²)/2`, determinant `(1-x²-z²)/4`, and *covariant* Born probabilities. Detector flips with known symmetric error `f<1/2` attenuate the expectation by `1-2f`; the model reports both the observed expectation and its exact calibrated value. At `f=1/2`, calibration is impossible and the program rejects it.

```sh
python3 -m unittest discover -s m45-st61 -p 'test_*.py'
python3 m45-st61/invariants.py --x 3/5 --z 4/5 --word HZ --axis Z --flip 1/10
```

**Scope:** Real Bloch XZ disk, finite H/Z frame group, ideal expectation values, known symmetric detector noise, exact bounded rational arithmetic. This is a *passive frame transformation* of state and measurement axis together. It does **not** claim that two observers measuring different untransported physical observables see identical statistics, nor that stochastic measurement outcomes match. It does not model unknown detector biases, full SU(2), relativity, measurement collapse, or prove a philosophical definition of objectivity. The PR remains a draft until review and CI verification.
