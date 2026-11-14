# M45-ST/63 — Relational U(1) Quantum Reference Frames

This stage introduces **two quantum systems**: a reference qubit A and a system qubit B. Each begins in an equatorial state `(|0>+exp(i phi)|1>)/sqrt(2)`, with phases alpha and beta. The joint state has four computational-basis amplitudes.

If no external absolute phase reference is available, we model that limitation by a **collective U(1) twirl**. This averages over a shared phase rotation and deletes density-matrix coherence between sectors of different total excitation number. Within the one-excitation subspace spanned by `|01>` and `|10>`, coherence survives:

`rho_twirled[01,10] = exp(i(beta-alpha))/4`.

A shared phase shift `alpha -> alpha+delta`, `beta -> beta+delta` leaves the twirled joint density matrix unchanged, while changing the **relative** phase `beta-alpha` changes the surviving relational coherence. The normalized state conditioned on the one-excitation sector is pure, even though the globally twirled state has purity 3/8.

```sh
python3 -m unittest discover -s m45-st63 -p 'test_*.py'
python3 m45-st63/relational_frames.py --alpha 0.2 --beta 1.1 --shift 0.7
```

**Scientific limits:** This is a U(1)-symmetry relational toy model with two qubits and an idealized absence of an external phase standard. The twirl represents a change in description/available reference information, **not necessarily a physical decoherence process**. The program does not implement a general quantum reference-frame switch, quantum clocks, gravity, Lorentz boosts, observer-independent measurement outcomes, or collapse. Conditional states depend on selecting a superselection sector; this is not a laboratory postselection demonstration. The shared-shift invariance is verified numerically to 1e-10. Read-only CI.
