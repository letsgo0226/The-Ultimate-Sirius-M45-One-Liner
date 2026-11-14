# M45-ST/49 — Decoherence and observational-type operators

A small **offline mathematical simulation** connecting the user's micro/macro and observational-type hypotheses to standard quantum formalism.

For a qubit in the Z basis, the model starts with
`rho = [[p, sqrt(p(1-p))], [sqrt(p(1-p)), 1-p]]`.
The dephasing channel `D_gamma` multiplies off-diagonal terms by `gamma` (0 ≤ gamma ≤ 1), leaving populations unchanged. This is a completely positive trace-preserving map for this parameter range.

It then calculates Born probabilities for **two incompatible measurement contexts**, X and Z, and checks Hermiticity, trace one, and positivity. With p=0.5 and gamma=0, the X-plus probability changes from 1 to 0.5 while the Z-plus probability stays at 0.5.

```sh
python3 -m unittest discover -s m45-st49 -p 'test_*.py'
python3 m45-st49/decoherence.py --p 0.5 --gamma 0.25
```

**Interpretation limits:** Decoherence is not proof of objective collapse, a unique outcome, macro-universe generation, or the universe being software. The model uses a fixed preferred Z basis and a single-qubit phase-damping channel; it is not a full environment simulation. Its output is calculated, not measured astrophysical data. No particles are physically prepared, and no external instruments are controlled.

The GitHub workflow is read-only and runs offline tests; it does not modify ST47's state or run continuously. This stage is stacked on ST48 and is intentionally a separate research module.
