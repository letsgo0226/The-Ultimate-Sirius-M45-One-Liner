# Translation symmetry and energy–momentum: free scalar baseline

Before tackling the **interacting** scalar–gauge system, this stage checks the translation Noether identity for the free real scalar doublet in 3+1 Minkowski spacetime (signature `+---`).

For `L=1/2 ∂_mu phi·∂^mu phi - 1/2 m² phi·phi`, define the canonical mixed tensor

```text
T^mu_nu = ∂^mu phi·∂_nu phi - delta^mu_nu L.
E_phi = (box + m²) phi.
∂_mu T^mu_nu = E_phi·∂_nu phi.    (off shell)
```

Hence `∂_mu T^mu_nu=0` on shell. This is a **local** conservation equation; conserved integrated charges require suitable spatial boundary conditions, falloff, and integrability. The code uses exact rational polynomial fields and checks the off-shell identity and simple on-shell examples, not spacetime integrals.

**Important limitation:** This is only the free scalar sector, not yet the total gauge-invariant energy–momentum tensor of the coupled charged scalar + Maxwell system. For gauge fields, the canonical tensor is not generally gauge invariant; a suitable improved/Hilbert tensor and careful sign conventions are needed. A future step should derive the coupled tensor from metric variation and verify its divergence using the coupled Euler–Lagrange equations. Do not claim total interacting energy conservation from this file alone.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/stress_energy_free_scalar_3p1.py
```

Research-only draft PR #67, not a unified physics theory; independent review required, no merge/deploy/spending/secrets.
