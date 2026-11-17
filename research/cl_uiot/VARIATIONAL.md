# From a Lorentz-invariant action to Klein–Gordon

In flat 1+1-dimensional Minkowski spacetime with signature (+,-), c=1, consider a **real classical free scalar field** and the Lagrangian density

```text
L(phi, ∂phi) = 1/2 [ (∂t phi)^2 - (∂x phi)^2 - m² phi² ].
S[phi] = ∫ L dt dx.
```

For smooth variations δφ of compact support (or boundary conditions making the surface term vanish), stationarity `δS=0` yields the Euler–Lagrange equation

```text
∂L/∂phi - ∂t(∂L/∂(∂t phi)) - ∂x(∂L/∂(∂x phi)) = 0
⇒ -(∂t²−∂x²+m²)phi = 0
⇒ (□+m²)phi = 0.
```

This **derives a known equation from an explicitly chosen action**, not the action uniquely from invariance. Many inequivalent Lorentz-invariant actions exist.

Under proper Lorentz transformations with determinant +1, the scalar field pullback and Minkowski metric imply `L'(x')=L(B⁻¹x')`; the volume measure is preserved, so the action is invariant when the transformed integration domain and boundary data are treated consistently.

The executable example uses exact rational polynomial fields, rational boosts `v=0,±3/5`, and a direct symbolic implementation of the Euler–Lagrange expression. It checks finite cases; it **does not integrate over spacetime, implement boundary conditions, prove existence of stationary fields, or constitute a general machine-checked theorem**.

### Reproduction

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/variational_kg_1p1.py
```

This is an educational research step within draft PR #67, not a Theory of Everything, quantum field theory, general relativity, or a new physical prediction. Independent review remains necessary; no production deployment or PR merge.
