# M45-ST/67 — Relational Quantum Information Geometry

This stage extends ST64–ST66 with **pairwise geometry of pure relational quantum states**. Two normalized complex four-component state vectors are compared in A-frame coordinates and again after both are transported by the same ST64 finite-Z2 frame switch.

For `F=|<psi|phi>|²`, we compute:
- **Transition fidelity:** `F`.
- **Pure-state trace distance:** `D=sqrt(1-F)`.
- **Fubini–Study angle:** `theta=acos(sqrt(F))`.
- **Bures distance:** `d_B=sqrt(2*(1-sqrt(F)))`.

All four are invariant under a **common unitary** frame switch. The code additionally compares the two states' probabilities for the transported relational event `B=C`. The resulting classical total-variation distance `TV=|p_psi-p_phi|` obeys `TV<=D` (measurement data processing).

```sh
python3 -m unittest discover -s m45-st67 -p 'test_*.py'
python3 m45-st67/information_geometry.py --first 1 0 1 0 --second 1 0 0 1
```

**Scope:** pure states in the ST64 global-Z2-even relational subspace, shared finite unitary frame switches, and a single binary relational measurement. Fidelity and distances are conventional established quantum information quantities; their invariance follows from unitarity and is not evidence of a new physical geometry. No mixed-state Uhlmann fidelity, quantum Fisher information, quantum gravity, physical collapse or general continuous quantum reference-frame transformation is implemented. Floating-point assertions use tolerance 1e-10. Read-only CI; CI and tests still need independent execution.
