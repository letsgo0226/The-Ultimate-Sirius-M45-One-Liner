# M45-ST/58 — Spectrum Broadcast Structure (Finite Diagonal Prototype)

This stage constructs an **actual finite-dimensional density operator** (represented by its complete diagonal) for a system pointer bit and N environment qubits:

`rho_SE = p |0><0| ⊗ tau_0^⊗N + (1-p) |1><1| ⊗ tau_1^⊗N`

with `tau_0=diag(1-q,q)`, `tau_1=diag(q,1-q)`, `0<=q<=1/2`. The operator is diagonal, positive and trace one. The program reports its full diagonal, von Neumann entropies (Shannon entropies of the eigenvalues), and quantum mutual information `I(S:E)=S(S)+S(E)-S(SE)`.

A *constructed* spectrum broadcast structure (SBS) requires that environment conditional states for distinct pointer values have orthogonal support in each fragment, `tau_0 tau_1=0`. In this model this occurs exactly at `q=0`. For `q>0`, there can be substantial accessible information but **not exact SBS**. `q=1/2` provides no information about S.

```sh
python3 -m unittest discover -s m45-st58 -p 'test_*.py'
python3 m45-st58/spectrum_broadcast.py --n 3 --p 0.5 --q 0.1
```

**Limitations:** The pointer basis, conditional independence and diagonal density matrix are **assumed by construction**, not dynamically derived from the unitary system-environment interaction of ST56. There is no quantum discord calculation, no off-diagonal coherences, no general many-body quantum simulation, no proof of objective collapse, and no inference that the universe is literally a computer. For p=0 or p=1 only one pointer value has nonzero prior; the orthogonality diagnostic still tests the two defined conditional states as a structural property. The complete diagonal grows exponentially, so n is bounded to 8. Read-only CI.
