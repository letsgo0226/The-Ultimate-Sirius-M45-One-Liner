# M45-ST/64 — Finite Quantum Reference Frame Switching (Z2 Toy Model)

This stage implements a **genuine change of relational coordinates for three qubits A, B and C** in a tightly restricted finite-symmetry setting. A simultaneous flip `(a,b,c)->(a XOR 1,b XOR 1,c XOR 1)` is treated as an unobservable global Z2 transformation.

An A-referenced description uses `u=b XOR a`, `v=c XOR a`; a B-referenced description uses `u'=a XOR b=u`, `v'=c XOR b=u XOR v`. The induced quantum frame switch is a **unitary permutation** of four complex relational amplitudes `psi_A[u,v] -> psi_B[u,u XOR v]`. Switching twice returns the original amplitudes.

To give these amplitudes a three-qubit interpretation, the model embeds the four-dimensional relational state in the **+1 eigenspace of the global X⊗X⊗X flip**, assigning equal amplitudes to both members of each global-flip orbit. This preserves coherent superpositions and is not merely a classical probability relabeling.

The relational projector for `B=C` has A-frame condition `u=v` and B-frame condition `v'=0`. Its Born probability is unchanged under the frame switch. Global-phase changes also preserve the relational density operator. The script reports full complex amplitudes for the lifted 8-dimensional state, A-frame and B-frame states, the relational probability and numerical invariant errors.

```sh
python3 -m unittest discover -s m45-st64 -p 'test_*.py'
python3 m45-st64/frame_switch.py --amplitudes 1 1j 2 -1 --phase 0.37
```

**Scope and limitations:** This is a finite Z2 toy model restricted to the global-flip-even sector. It does **not** implement general non-Abelian or continuous quantum reference-frame transformations, quantum uncertainty of a continuous reference orientation, quantum clocks, Lorentz boosts, or full general-relativistic covariance. It does not derive a measurement outcome or prove philosophical objectivity. The invariant concerns a relational observable under a consistent change of frame, not arbitrary distinct measurements. Standard-library only; read-only CI.
