# Conformal geometry and curved scalar equation (3+1)

For a prescribed conformal metric `g_mu nu=Omega² eta_mu nu` on a patch where `Omega>0`, with `eta=diag(+---)`, the Levi-Civita connection is

```text
Gamma^rho_mu nu = Omega^-1 [
 delta^rho_mu ∂_nu Omega + delta^rho_nu ∂_mu Omega
 - eta_mu nu eta^rho rho ∂_rho Omega
].
```

The Ricci tensor and scalar are

```text
R_mu nu = -2 Omega^-1 ∂_mu∂_nu Omega
          +4 Omega^-2 (∂_mu Omega)(∂_nu Omega)
          -eta_mu nu [Omega^-1 Box_eta Omega
                     +Omega^-2 (∂Omega)²_eta],

R = -6 Omega^-3 Box_eta Omega.
```

The exact rational polynomial implementation avoids division by computing `Omega Gamma`, `Omega² Ricci`, and `Omega³ R`. It checks `eta^{mu nu}(Omega² R_mu nu)=Omega*(Omega³ R)` and the curved scalar relation

```text
Omega⁴ (Box_g+m²)phi
 = Omega² Box_eta phi + 2 Omega ∂^mu Omega ∂_mu phi
   + Omega⁴ m² phi
 = ∂_mu(Omega² ∂^mu phi)+Omega⁴ m² phi.
```

The tests include symmetry, flat limit, nonzero curvature, vanishing Ricci scalar with potentially nonzero Ricci tensor, polynomial monomials, and the scalar equation identity. They are finite algebraic checks, **not** a general proof assistant verification. No independent Riemann-tensor or Bianchi-identity implementation is claimed here.

**Limits:** conformal flatness restricts the metric; Omega positivity is assumed on the physical patch, not globally certified by the polynomial engine. Curvature is prescribed, not dynamical; no Einstein–Hilbert variation, gravitational backreaction, or Einstein field equations are derived. This does not establish a Theory of Everything.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/conformal_geometry_3p1.py
```

Research-only draft PR #67. No merge, deployment, spending, secret access, or self-approval.
