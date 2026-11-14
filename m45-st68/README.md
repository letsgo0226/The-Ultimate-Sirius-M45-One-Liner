# M45-ST/68 — Quantum Fisher Information and Relational Metrology

This stage extends ST64's finite-Z2 relational frame switch and ST67's information geometry with a continuously encoded parameter **theta**.

A normalized A-frame pure relational state `|psi>` undergoes `exp(-i theta G_A)`, where `G_A=(I tensor X)/2` acts on the second relational qubit. The B-frame description uses the transported state and **transported generator** `G_B=U G_A U†`, where `U` is ST64's unitary reference switch. It is incorrect to keep the original generator fixed when changing frames.

For this pure unitary family, the quantum Fisher information is `F_Q=4 Var(G)=1-<I tensor X>²`. The implementation verifies equality of QFI in A and B frames. A transported relational binary event `B=C` gives a probability `p(theta)`, derivative `dp/dtheta`, and classical Fisher information `F_C=(dp/dtheta)²/[p(1-p)]` when `0<p<1`. The program checks `F_C<=F_Q`.

The default initial state `(|00>+i|01>)/sqrt(2)` has `F_Q=1`. For nonboundary parameter values, the chosen binary relational measurement also attains `F_C=1`. For `nu` independent identically prepared copies, the quantum Cramér–Rao lower bound is `Var(theta_hat)>=1/(nu F_Q)` **under the usual local unbiasedness and regularity assumptions**. The JSON reports the `nu=1` formal bound, not a guaranteed finite-sample estimator variance.

```sh
python3 -m unittest discover -s m45-st68 -p 'test_*.py'
python3 m45-st68/quantum_metrology.py --amplitudes 1 1j 0 0 --theta 0.3
```

**Scope:** finite global-Z2-even relational sector; pure states; single-parameter unitary encoding; local estimation. This is established quantum metrology applied to a finite frame-change model, not a discovery of new measurement precision, a proof of universal observer agreement, or a general quantum reference-frame transformation. Binary Fisher information is left undefined at probability boundaries instead of silently reporting an incorrect finite value. Read-only CI; execution and review pending.
