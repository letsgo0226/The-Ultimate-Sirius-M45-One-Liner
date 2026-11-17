# Restricted Einstein–Hilbert variation in a conformal 3+1 ansatz

For a prescribed conformal family `g_mu nu=Omega² eta_mu nu`, on a patch where `Omega>0` and `eta=(+---)`, the gravitational Einstein–Hilbert scalar density (omitting its constant coupling factor) is

```text
sqrt(-g) R = Omega⁴ (-6 Omega^-3 Box_eta Omega)
           = -6 Omega Box_eta Omega.
```

Varying only `Omega` gives the exact off-shell identity

```text
delta(sqrt(-g) R)
 = -12 deltaOmega Box_eta Omega
   -6 partial_mu [Omega partial^mu deltaOmega
                  - deltaOmega partial^mu Omega].
```

With compactly supported variations or suitable boundary terms, the restricted Euler–Lagrange equation is `Box_eta Omega=0`. This is **only the trace/conformal projection** of the vacuum Einstein equations, not their full ten independent components. In particular, `R=0` does not imply `R_mu nu=0` or `G_mu nu=0`; even a linear nonconstant Omega can have vanishing scalar curvature and nonzero Ricci tensor.

Using the independent conformal curvature module, the functional derivative satisfies

```text
delta S_EH / delta Omega = 2 Omega³ R = -12 Box_eta Omega.
```

The equality with the trace follows from the standard inverse-metric variation `delta(sqrt(-g)R)=sqrt(-g)G_mu nu delta g^{mu nu}+boundary`, with `delta g^{mu nu}=-2 Omega^-3 eta^{mu nu}deltaOmega`. This is a **consistency check** of a known variation formula, not an independent derivation for arbitrary metric perturbations. A complete gravitational variational principle requires treatment of boundary conditions (often a Gibbons–Hawking–York term), arbitrary metric variations, and matter coupling.

The Python tests check exact rational polynomial identities and flat limits. They are not a proof assistant verification, Einstein equation solver, or physical unification claim.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/conformal_einstein_hilbert_3p1.py
```

Research-only draft PR #67; no merge, deployment, secret use, spending, or self-approval.
