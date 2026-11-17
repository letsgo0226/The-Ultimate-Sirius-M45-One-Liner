# Einstein tensor and contracted Bianchi identity on conformal 3+1 backgrounds

This stage builds on `CONFORMAL_GEOMETRY_3P1.md`. For a prescribed Lorentzian metric `g_mu nu=Omega² eta_mu nu` with `Omega>0` on the chosen patch and signature `+---`, define

```text
G_mu nu = R_mu nu - (1/2) g_mu nu R.
E_mu nu := Omega² G_mu nu
         = (Omega² R_mu nu) - (1/2) eta_mu nu Omega*(Omega³ R).
```

The exact polynomial code computes `E_mu nu`, so no division by `Omega` is required. In four spacetime dimensions its trace satisfies

```text
eta^mu nu E_mu nu = -Omega*(Omega³ R).
```

For a symmetric mixed tensor `G^mu_nu`, the contracted Bianchi identity `nabla_mu G^mu_nu=0` is equivalent on the conformal patch to the polynomial identity

```text
Omega * sum_mu eta[mu] partial_mu E_mu nu
 - sum_mu,rho eta[mu] (Omega Gamma^rho_mu nu) E_mu rho = 0.
```

Derivation: `sqrt(-g)=Omega⁴`, `G^mu_nu=eta[mu] E_mu nu/Omega⁴`, and `Gamma^rho_mu nu=(Omega Gamma^rho_mu nu)/Omega`. Use `nabla_mu G^mu_nu = (1/sqrt(-g)) partial_mu(sqrt(-g) G^mu_nu) - Gamma^rho_mu nu G^mu_rho`; multiplying by `Omega⁵` yields the tested polynomial residual.

This is a **geometric identity**, not an equation of motion. It implies a consistency condition for any subsequently postulated equation `G_mu nu=8 pi G_N T_mu nu`: its source must be covariantly conserved, but neither Einstein's equation nor gravitational dynamics follows from the identity alone.

Tests cover symmetry, trace, flat limit, nonconstant conformal factors, and all four divergence components. They are finite exact algebraic checks, not a Lean proof of the general differential-geometric Bianchi identity. There is no arbitrary metric engine, Einstein–Hilbert variation, dynamical backreaction, or demonstrated physical unification.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/conformal_einstein_bianchi_3p1.py
```

Research-only draft PR #67; no merge, deployment, expenditure, secrets, or self-approval.
