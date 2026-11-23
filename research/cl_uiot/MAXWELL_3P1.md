# 3+1 Maxwell theory: exact polynomial research stage

We extend the earlier 1+1 Abelian model to four coordinates `(t,x,y,z)` with metric signature `(+---)`. A covariant potential `A_mu` has four components. The field strength is `F_mu nu=∂_mu A_nu−∂_nu A_mu`, and the classical free-field Lagrangian is `L=-1/4 F_mu nu F^mu nu`.

The exact rational polynomial implementation checks:

- **Local Abelian gauge invariance:** `A_mu → A_mu+∂_mu chi` leaves `F` and `L` unchanged.
- **Bianchi identity:** `∂_lambda F_mu nu+∂_mu F_nu lambda+∂_nu F_lambda mu=0`.
- **Conservation identity:** for the induced off-shell current `j^nu=∂_mu F^{mu nu}`, `∂_nu j^nu=0`.

These are algebraic identities based on commuting partial derivatives. They do **not** assert that an arbitrary `A` satisfies the source-free Maxwell equations: `j` generally is nonzero. With a prescribed source, solving `∂_mu F^{mu nu}=j^nu` requires additional initial/boundary conditions and a PDE solver.

The earlier U(1) doublet and scalar-field action are not yet combined into a single minimally coupled dynamical action. The next separate milestone is `L = 1/2 (D_mu phi)^T eta^{mu nu}(D_nu phi) - 1/2 m² phi^T phi - 1/4 F_mu nu F^mu nu` for a real scalar doublet, with the gauge transformation conventions aligned. A finite polynomial check of infinitesimal covariance would not establish quantum electrodynamics or unification.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/maxwell_3p1.py
```

This is a classical 3+1 flat-spacetime toy model, not a full Standard Model, general relativity, or a Theory of Everything. It remains in draft PR #67 pending independent review.
