# Total stress tensor for coupled classical scalar + U(1) fields

This is the next research step beyond the **free** scalar translation tensor. Signature `eta=(+---)`, `D_mu phi=partial_mu phi+q A_mu J phi`, `F_mu nu=partial_mu A_nu-partial_nu A_mu`, and the same chosen coupled Lagrangian `L=L_matter+L_gauge`.

The mixed-index, gauge-invariant symmetric stress tensor is

```text
T^mu_nu = (D^mu phi)·(D_nu phi)
         - F^{mu rho} F_{nu rho}
         - delta^mu_nu L.
```

It is symmetric after raising the second index with the Minkowski metric. With the field residuals

```text
E_phi = D_mu D^mu phi + m² phi,
R_A^rho = partial_mu F^{mu rho} - j^rho,
j^rho = -q (D^rho phi)·(J phi),
```

the off-shell identity is

```text
partial_mu T^mu_nu = E_phi·D_nu phi - R_A^rho F_{nu rho}.
```

Hence, if **both** coupled equations hold, `partial_mu T^mu_nu=0`. The two sectors exchange energy-momentum through the gauge interaction; only the total tensor has the displayed on-shell conservation law in general. Local conservation does not guarantee finite, conserved spatially integrated charges without appropriate falloff/boundary assumptions.

The code checks the identity for finite exact rational polynomial examples and includes an electric-field positive-energy test. **These tests are not a proof-assistant proof, a general existence theorem, quantization, or a new theory of fundamental interactions.** Sign conventions, metric variation, and boundary terms should receive independent human review before scientific claims.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/stress_energy_coupled_3p1.py
```

Research-only draft PR #67. No merge, deployment, expenditure, secret use, or self-approval.
