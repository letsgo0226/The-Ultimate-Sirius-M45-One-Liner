# Klein–Gordon covariance: exact 1+1 polynomial model

Let `η=diag(1,-1)`, `c=1`, `□=∂_t²−∂_x²`, and `D=□+m²`. For a proper Lorentz boost `B`, a scalar field transforms as `φ'(x')=φ(B⁻¹x')`. Then

```text
D' φ'(x') = (D φ)(B⁻¹x').
```

The equality follows from the chain rule and `BᵀηB=η`. Here the operator has the same coordinate expression in both inertial frames; this is *covariance*, not a proof that every individual field is invariant.

The exact rational polynomial program implements `φ(t,x)` as a finite dictionary of monomial coefficients and computes both sides, with rational boosts `v=0,±3/5`. It tests the Klein–Gordon operator including `m²`, polynomial examples, and a counterexample for a non-Lorentz scaling. **Tests over finite samples are not a machine-checked general proof.** The mathematical argument relies on standard chain-rule reasoning and the metric identity.

### Physical boundaries

This is a free scalar field in flat 1+1 spacetime, not a new unified field equation, not curved-spacetime general covariance, not quantization, not interactions, and not an empirical prediction. It also does not assert the existence of nonzero KG solutions with any particular boundary conditions.

### Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/klein_gordon_1p1.py
```

This extension remains part of draft PR #67, with independent review and no deployment or merge.
