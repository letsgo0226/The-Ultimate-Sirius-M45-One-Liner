# Independent metric-variation audit of the coupled stress tensor

We audit the earlier coupled scalar–U(1) energy–momentum tensor by an **independent algebraic route** rather than reusing its divergence identity. At the flat Minkowski metric `g^{mu nu}=diag(+---)`, use the classical Lagrangian

```text
L(g) = (1/2) g^{mu nu} (D_mu phi)·(D_nu phi)
       - (1/2) m² phi·phi
       - (1/4) g^{mu rho} g^{nu sigma} F_mu nu F_rho sigma.
```

Holding the covariant field components and derivatives fixed during metric variation, define the Hilbert tensor with the convention

```text
T_mu nu = 2 partial L / partial g^{mu nu} - g_mu nu L.
```

This matches the earlier mixed-index expression after raising the first index. The code varies each of the 10 independent components of the **symmetric inverse metric**; for off-diagonal entries it varies both mirrored entries and accounts for the factor of two. Since `L(g)` is at most quadratic in the inverse metric, the central difference at `epsilon=±1` extracts its exact linear coefficient over rational polynomials. All 16 ordered tensor components are compared with the independently constructed stress tensor.

This is an algebraic flat-metric consistency check, **not** a full curved-spacetime derivation: it does not implement the volume factor `sqrt(-g)`, a Levi-Civita connection, dynamical gravity, Einstein equations, or boundary terms. For a generally covariant action, variation of `sqrt(-g)L` supplies the `-g_mu nu L` term in the stated convention. The convention should be independently reviewed before extending to curvature.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/metric_variation_audit_3p1.py
```

Research-only draft PR #67. Tests are not a general formal proof or a Theory of Everything. No merge, deployment, secret use, spending, or self-approval.
