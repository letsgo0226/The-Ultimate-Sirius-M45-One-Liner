# M45-ST/66 — Relational Quantum Information Conservation

This stage extends ST64's finite three-qubit global-Z2-even sector and ST65's frame-dependent entanglement. A frame switch is a unitary permutation of four complex relational amplitudes, corresponding to CNOT on the relational two-factor Hilbert space.

For each frame we calculate the reduced density matrices of both relational factors by partial trace. Reported quantities include reduced purity, subsystem von Neumann entropy (bits), and mutual information `I(1:2)=S(1)+S(2)-S(12)`. The **joint relational state is pure** in both frames, so `S(12)=0` and `Tr(rho_joint²)=1`.

The default A-frame state `(|00>+|10>)/sqrt(2)` is a product, with subsystem entropies 0 and mutual information 0 bits. Switching to B-frame coordinates maps it to `(|00>+|11>)/sqrt(2)`, with subsystem entropies 1 bit each and mutual information 2 bits. **This is not physical information creation**: the frame switch changes which tensor factors count as subsystems.

The relational probability of `B=C` remains invariant when its projector is expressed in each frame. The implementation verifies global purity, global entropy, both local entropies' equality for pure bipartite states, inverse switching and relational probability consistency.

```sh
python3 -m unittest discover -s m45-st66 -p 'test_*.py'
python3 m45-st66/information_conservation.py --amplitudes 1 0 1 0
```

**Scope:** pure states only; a finite global-Z2 symmetry and its even sector; two-factor relational decompositions; exact frame-permutation logic with floating-point entropy evaluation. The word “conservation” refers to invariant global state spectrum and consistently transported relational observables, not a general theorem that all notions of quantum information are conserved, or a new physical conservation law. No general quantum reference frames, physical entanglement generation, collapse, thermodynamic entropy conservation, or spacetime covariance is claimed. Read-only CI; results require verification.
