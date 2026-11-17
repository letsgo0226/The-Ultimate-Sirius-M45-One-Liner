# Nonconstant conformal metric: curved-background scalar variational test

This is a **controlled extension beyond flat spacetime**, not yet a fully general curved-spacetime theory. Take a prescribed Lorentzian conformal metric in four dimensions:

```text
g_mu nu = Omega(x)^2 eta_mu nu, Omega(x)>0,
g^mu nu = Omega(x)^(-2) eta^mu nu,
sqrt(-det g) = Omega(x)^4.
```

For a free real scalar doublet, the covariant action density simplifies to a polynomial expression without division:

```text
L_density = 1/2 Omega² eta^mu nu ∂_mu phi·∂_nu phi
            - 1/2 Omega⁴ m² phi·phi.
E_density = ∂_mu(Omega² ∂^mu phi) + Omega⁴ m² phi.
```

The local first-variation identity is

```text
delta L_density = -delta phi·E_density
  + ∂_mu[Omega² (∂^mu phi)·delta phi].
```

For compactly supported variations or suitable boundary conditions, stationarity gives `E_density=0`. On a patch where `Omega>0`, this is equivalent to `(Box_g + m²)phi=0`, with `Box_g phi = (1/sqrt(-g)) ∂_mu(sqrt(-g) g^mu nu ∂_nu phi)`. The polynomial tests do not enforce global positivity of Omega; interpret the chosen Omega only on a positive patch.

The tests cover a nonconstant conformal factor, massless and massive cases, polynomial monomials, and the exact flat `Omega=1` limit. The background is prescribed: **no metric dynamics, Einstein–Hilbert action, curvature tensor computation, coupled gauge-field curved equations, or gravitational field equations** are implemented. Conformal flatness is a restricted class of metrics; general covariance is not established by these examples.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/conformal_scalar_3p1.py
```

Research-only draft PR #67. Independent review required; no merge, deployment, spending, secret use, or self-approval.
