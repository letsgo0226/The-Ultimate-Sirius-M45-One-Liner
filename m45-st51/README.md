# M45-ST/51 — Observational Invariants

This stage tests which properties survive a **change of the Z-basis dephasing parameter** in the ST49/ST50 independent-qubit model.

For fixed N and p, changing gamma preserves:
- Trace one of the qubit density matrix.
- Z-basis Born probabilities.
- Binomial macro Z-count distribution, mean and variance.

For a nontrivial coherent initial state, changing gamma generally alters:
- X-basis Born probabilities.
- The l1 norm of off-diagonal coherence.

Example:
```sh
python3 m45-st51/invariants.py --n 32 --p 0.7 --gamma-a 0 --gamma-b 1
python3 -m unittest discover -s m45-st51 -p 'test_*.py'
```

**Scope:** This is not a proof that all physical observers agree on macro reality. The invariants hold because the selected dephasing channel leaves Z populations unchanged, and the macro count is computed in that same Z basis for independent qubits. A different measurement basis, interaction, channel, or coarse-graining rule may change the conclusion. In particular, equality of gamma or a Z eigenstate need not exhibit changes in X statistics.

This model does not establish objective wavefunction collapse, a physical universe-as-computer ontology, or new astronomical observations. Read-only CI; no persistent actions or physical devices.
