# Linearized Einstein tensor around Minkowski spacetime

Unlike the previous conformal ansatz, this stage admits **all ten independent components** of a symmetric perturbation `h_mu nu`, with `g_mu nu=eta_mu nu+epsilon h_mu nu+O(epsilon²)` and `eta=diag(+---)`.

At first order, with `h=eta^mu nu h_mu nu`, the linearized Ricci tensor and scalar are

```text
R^(1)_mu nu = 1/2 (partial_rho partial_mu h^rho_nu
                   + partial_rho partial_nu h^rho_mu
                   - Box_eta h_mu nu
                   - partial_mu partial_nu h),

R^(1) = eta^mu nu R^(1)_mu nu,
G^(1)_mu nu = R^(1)_mu nu - 1/2 eta_mu nu R^(1).
```

The exact rational polynomial tests check the **linearized contracted Bianchi identity**

```text
partial^mu G^(1)_mu nu = 0
```

and invariance under infinitesimal linearized coordinate/gauge shifts

```text
h_mu nu -> h_mu nu + partial_mu xi_nu + partial_nu xi_mu.
```

The overall sign of the infinitesimal coordinate convention can be reversed without changing gauge invariance. The perturbations are not restricted to conformal multiples of the Minkowski metric. This directly addresses the limitation exhibited in `CONFORMAL_TRACE_COUNTEREXAMPLE_3P1.md`.

**Scope:** This computes only the coefficient linear in `epsilon`. It does not construct the nonlinear Einstein tensor, prove existence of solutions, couple matter, fix gauge, quantize gravitons, or derive the full Einstein–Hilbert action by arbitrary metric variation. Exact finite polynomial regression tests are not a proof-assistant verification.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/linearized_einstein_3p1.py
```

Research-only draft PR #67. No merge, deployment, spending, secrets, or self-approval.
