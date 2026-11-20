# Harmonic gauge and trace-reversed linearized Einstein equations

Continue the arbitrary symmetric perturbation `g_mu nu=eta_mu nu+epsilon h_mu nu+O(epsilon²)` around Minkowski spacetime (`eta=diag(+---)`). Define the trace reverse

```text
bar_h_mu nu = h_mu nu - (1/2) eta_mu nu h,
h = eta^mu nu h_mu nu.
```

In four dimensions trace reversal is an involution. Introduce the harmonic-gauge constraint

```text
C_nu = partial^mu bar_h_mu nu.
```

Without assuming the constraint vanishes, the exact first-order identity is

```text
G^(1)_mu nu = -1/2 Box_eta bar_h_mu nu
  + 1/2 [partial_mu C_nu + partial_nu C_mu
         - eta_mu nu partial^rho C_rho].
```

Thus in harmonic gauge `C_nu=0`, `G^(1)_mu nu=-1/2 Box_eta bar_h_mu nu`. If one **additionally postulates** the linearized Einstein equation `G^(1)_mu nu=8 pi G_N T_mu nu` (units `c=1`), then

```text
Box_eta bar_h_mu nu = -16 pi G_N T_mu nu.
```

This wave equation is not derived solely from gauge fixing. The source must satisfy `partial^mu T_mu nu=0` at this perturbative order. Under a linearized gauge shift `h_mu nu -> h_mu nu + partial_mu xi_nu + partial_nu xi_mu`, the constraint changes by `C_nu -> C_nu + Box_eta xi_nu`. Finding a gauge-fixing xi requires solving an appropriate wave equation with boundary/initial conditions; this code does not assert that such a solution exists for arbitrary inputs.

The exact rational polynomial tests check the full off-gauge decomposition, trace reversal involution, and constraint transformation. They do not implement wave propagation, gravitational radiation, arbitrary nonlinear gravity, or quantum gravity.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/harmonic_linearized_gravity_3p1.py
```

Research-only draft PR #67. No merge, deployment, spending, secret use, or self-approval.
