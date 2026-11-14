# M45-ST/65 — Relational Entanglement and Frame-Dependent Subsystems

This stage extends the finite three-qubit global-Z2 relational frame switch from ST64. The A-frame relational coordinates are `u=B XOR A`, `v=C XOR A`; the B-frame coordinates are `u'=A XOR B=u`, `v'=C XOR B=u XOR v`. On the **two-qubit relational Hilbert space**, switching frames is the CNOT permutation `|u,v> -> |u,u XOR v>`.

This operation is unitary but **not local with respect to the original two-factor decomposition**. Therefore the entanglement attributed to the coordinate factors can change under a change of relational frame. We calculate pure-state concurrence `C=2|ad-bc|` for amplitudes `(a,b,c,d)` and the corresponding one-factor von Neumann entropy `h2((1+sqrt(1-C²))/2)`.

The default A-frame state `(|00>+|10>)/sqrt(2)` is a product state (C=0, entropy 0). Under the B-frame switch, it is represented as `(|00>+|11>)/sqrt(2)` (C=1, entropy 1). This does **not** imply that a physical interaction created entanglement: the reference-dependent tensor factorization has changed.

The relational event `B=C` is expressed as `u=v` in A coordinates and `v'=0` in B coordinates. Its Born probability remains identical across both descriptions.

```sh
python3 -m unittest discover -s m45-st65 -p 'test_*.py'
python3 m45-st65/relational_entanglement.py --amplitudes 1 0 1 0
```

**Limits:** Pure states only; finite global-Z2-even sector; fixed two-factor coordinate decompositions; no general continuous quantum reference frames, no entanglement distillation, no spacetime covariance, no measurement-collapse model. A coordinate change cannot by itself be used as a physical entangling gate. Depends on ST64. Read-only CI; review and CI verification pending.
