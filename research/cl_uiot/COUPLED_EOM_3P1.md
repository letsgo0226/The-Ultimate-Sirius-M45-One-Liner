# Coupled Euler–Lagrange equations and Noether identity (3+1)

Starting from the **chosen** classical charged scalar doublet + Abelian gauge action in `COUPLED_SCALAR_U1_3P1.md`, with `eta=(+---)`, `J(a,b)=(-b,a)`, and `D_mu=partial_mu+q A_mu J`, varying the real scalar doublet gives

```text
E_phi := D_mu D^mu phi + m² phi = 0.
```

Varying the covariant gauge potential `A_nu` gives

```text
partial_mu F^{mu nu} = j^nu,
j^nu = -q (D^nu phi) dot (J phi).
```

These formulas assume smooth fields and compactly supported variations, or boundary conditions removing surface terms. The signs are fixed by `D=partial+qAJ` and `L_matter=1/2(Dphi)²-1/2 m²phi²`.

**Off-shell Noether identity** (holds even when equations of motion are not satisfied):

```text
partial_nu j^nu = -q E_phi dot (J phi).
```

The mass term cancels because `phi dot J phi=0`. Thus **on the scalar equations of motion** `E_phi=0`, the matter current is conserved. A generic polynomial field is *off shell* and need not have conserved matter current. Independently, the divergence of `partial_mu F^{mu nu}` vanishes identically; this makes current conservation necessary for a solution of the Maxwell equation.

The exact rational polynomial code computes the two equation residuals and the Noether identity. It tests finite examples including a trivial coupled solution and non-solutions; it does **not** numerically integrate the coupled PDE, establish general existence/uniqueness, quantize the theory, or infer a Theory of Everything. Its tests are not a formal proof in Lean.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/coupled_eom_3p1.py
```

Research-only draft PR #67. No merge, deployment, self-approval, funds, or secret use.
