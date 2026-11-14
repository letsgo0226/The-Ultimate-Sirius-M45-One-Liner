# M45-ST/57 — Redundant Environment Records (Quantum Darwinism Toy Prototype)

This bounded **classical record model** illustrates one operational ingredient of quantum Darwinism: multiple disjoint fragments of an environment can carry information about a system's pointer value.

A pointer bit S has probability `P(S=1)=p`. Each of N record bits independently copies S with bit-flip error probability `q <= 1/2`. For fragment size m, the program calculates accessible classical mutual information `I(S;F_m)=H(S)-H(S|F_m)` from the exact binomial likelihoods for the number of observed ones.

The program reports the information curve over m=0..N, the smallest m reaching a fraction `1-delta` of H(S), and the number `floor(N/m)` of disjoint fragments of that size. It reports no redundancy when the pointer entropy is zero or the information target is zero. This is a **model-defined** redundancy indicator, not a universal physical threshold.

```sh
python3 -m unittest discover -s m45-st57 -p 'test_*.py'
python3 m45-st57/redundant_records.py --n 12 --p 0.5 --q 0.1 --delta 0.1
```

**Scientific boundaries:** The program models *classical* conditional record distributions and does not evolve a many-body quantum state, model quantum discord, prove spectrum broadcast structure, or establish objective wavefunction collapse. Conditional independence and the pointer basis are assumed. In particular, this does not show that observer agreement proves a unique ontological outcome. GitHub Actions runs offline read-only tests; no instruments or physical particles are involved.
