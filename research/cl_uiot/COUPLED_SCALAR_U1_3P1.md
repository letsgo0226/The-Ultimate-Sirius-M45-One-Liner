# Coupled charged scalar and U(1) gauge field in 3+1 dimensions

This stage joins the previously separate **classical** real scalar doublet and Abelian gauge field in a single Lagrangian density. With metric `eta=diag(+1,-1,-1,-1)`, `J=[[0,-1],[1,0]]`, and `D_mu phi=partial_mu phi+q A_mu J phi`, choose

```text
L = (1/2) eta^{mu nu} (D_mu phi)·(D_nu phi)
    - (1/2) m² phi·phi
    - (1/4) F_mu nu F^{mu nu}.
```

For nonzero charge q, an infinitesimal local transformation is

```text
delta phi = alpha J phi,
delta A_mu = -(partial_mu alpha)/q.
```

The exact first-order identities are

```text
delta(D_mu phi) = alpha J (D_mu phi),
delta F_mu nu = 0,
delta L = 0.
```

The kinetic term is invariant because J is antisymmetric and `v·Jv=0`; the mass term is invariant for the same reason; the gauge-field term is invariant because mixed partials commute.

**What the code actually does:** exact rational polynomial calculations of these *first-order* identities for finite examples, plus tests of the wrong-sign potential transformation. It does not derive the coupled Euler–Lagrange equations, integrate an action over spacetime, solve a boundary-value problem, implement finite gauge transformations, quantize the fields, or derive empirical predictions. The chosen Lagrangian is not uniquely forced by symmetry alone.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/coupled_scalar_u1_3p1.py
```

Research-only draft PR #67. No merge, deployment, expenditures, secrets, or self-approval.
