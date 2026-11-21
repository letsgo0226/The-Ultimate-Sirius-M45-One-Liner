# Maxwell curvature and variational equation in 1+1 spacetime

For a classical Abelian gauge potential `A_mu=(A_0,A_1)` and Minkowski metric `eta=diag(1,-1)`, define

```text
F_01 = partial_t A_1 - partial_x A_0
F_10 = -F_01
L = -1/4 F_mu_nu F^mu_nu = +1/2 (F_01)^2.
```

The source-free Euler–Lagrange equation of the gauge action `S[A]=∫ L dt dx`, assuming compact-support variations or boundary terms that vanish, is

```text
partial_mu F^{mu nu} = 0.
```

In these sign conventions, the Euler–Lagrange expressions for `A_0,A_1` are `(partial_x F_01, -partial_t F_01)`. If an external conserved source is introduced with interaction density `-j^mu A_mu`, the equation becomes `partial_mu F^{mu nu}=j^nu` (the source term and boundary conditions are **not** implemented as an action in the program). Taking the divergence gives the necessary identity `partial_nu j^nu=0` by antisymmetry of `F` and commuting derivatives.

Under `A_mu → A_mu + partial_mu chi`, `F` and the free-field Lagrangian density are exactly invariant, since mixed partial derivatives commute. This is compatible with the previous infinitesimal U(1) convention by choosing `chi=-alpha/q`.

The exact rational polynomial program checks curvature, gauge invariance, the free Maxwell Euler–Lagrange expression, and conservation of the **induced** current `j^nu=partial_mu F^{mu nu}`. It does **not** solve Maxwell equations for arbitrary prescribed currents. In 1+1 dimensions, source-free Maxwell theory has no local propagating photon degrees of freedom, so this model cannot stand in for the phenomenology of 3+1 electromagnetism.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/maxwell_1p1.py
```

Research-only, no physical unification claim, independent review required; PR #67 remains draft, without deployment or merge.
