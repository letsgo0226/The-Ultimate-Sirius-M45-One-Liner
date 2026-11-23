# ACRRO-06: reversible finite tape prototype
ACRRO-05 passed CI 44917900177. State (q,h,t) has one control bit,
a cyclic head, and a binary tape of power-of-two length <=4096.
Local bijection (q,b)->(u,a)=(q XOR b,q) has inverse
(q,b)=(a,a XOR u). Move head by 1-2u modulo tape length.
Backward first undoes motion using u, then inverts local gate.
Both compositions are identity on valid states, without a history log.
Walsh update of a single cell uses delta*(-1)^popcount(k&h).
Native spectral updates validate the entire input via inverse transform;
there is no claim of improved asymptotic speed.
Tests enumerate 4244 states (4+16+128+4096)
and both inverse compositions, spectral conjugacy, and a 100-step roundtrip.
This is a finite reversible permutation, not a universal Turing machine,
and has no halting instruction. External step count is needed to undo
a chosen number of steps. Finite orbits are periodic. No demonstration
of hardware independence, infinite execution, or physical reversibility.
Lean verification pending. No merge or deployment.
