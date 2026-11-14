# M45-ST/55 — Emergent Classicality Operator (Operational Prototype)

ST55 combines two *separate* operational diagnostics:
1. **Small Z-basis coherence** of a dephased single-qubit density matrix, measured by `l1 = 2|rho_01|`.
2. **Reliable Z-majority macro outcome** for N independent, identically prepared qubits, measured by the exact binomial tail probability of a wrong or tied majority.

A run is labelled `operational_classicality` only when both user-defined tolerances are met. These tolerances are conventions, **not a universal definition of classicality**. When `p=1/2`, no preferred Z-majority is defined and the stability criterion is false.

The model also reports the fraction standard deviation `sqrt(p(1-p)/N)` and the Hoeffding upper bound `exp(-2N(p-1/2)^2)` on majority failure for `p != 1/2`. Dephasing changes coherence but does **not** change the Z majority probabilities in this model; increasing N can concentrate Z statistics but does **not** by itself destroy quantum coherence.

```sh
python3 -m unittest discover -s m45-st55 -p 'test_*.py'
python3 m45-st55/classicality.py --n 64 --p 0.7 --gamma 0.05
```

**Scope:** Product-state, independent qubits; a Z dephasing channel; Z-majority measurement; finite N <= 256. No entanglement, interacting many-body dynamics, decoherence environment, objective collapse, unique-outcome mechanism, or proof of the universe-as-computer hypothesis. No actual astronomical measurement or physical particle creation. GitHub Actions is read-only; ST47 persistence is not integrated.
