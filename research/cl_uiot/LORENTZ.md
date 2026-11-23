# Exact Lorentz covariance: a limited CL-UIOT example

This extension is a **1+1-dimensional special-relativistic algebra check**, not a derivation of gravity, quantum mechanics, or a Theory of Everything.

Use metric `η=diag(1,-1)` and units `c=1`. For speed `v=3/5`, the rational Lorentz factor is `γ=5/4`, and the boost is

```text
B = [[ 5/4, -3/4],
     [-3/4,  5/4]].
```

The exact identity `BᵀηB=η` gives `(Bk)ᵀη(Bk)=kᵀηk`. Consequently the relativistic mass-shell constraint `E²-p²=m²` is preserved. In the supplied example `k=(5,3)`, `m=4`, and `Bk=(4,0)`.

For the scalar Klein–Gordon differential operator `D=□+m²` in 1+1 flat spacetime, `□=∂ₜ²−∂ₓ²`, Lorentz covariance is consistent with the same metric invariance. **The executable program checks only finite-dimensional quadratic-form invariance and mass-shell algebra; it does not symbolically differentiate fields or establish PDE covariance.** A complete PDE proof would require specifying how scalar fields transform, derivatives under coordinate changes, domains, and boundary conditions.

The mass-shell quadratic form is not the same object as the differential operator; identifying them without specifying the Fourier/plane-wave correspondence would be incorrect.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/lorentz_1p1.py
```

The code supports only `v=0, ±3/5`, using exact rational arithmetic. Its tests are examples, not a general formal proof. This draft must remain under independent review and must not be represented as experimentally validated physics.
