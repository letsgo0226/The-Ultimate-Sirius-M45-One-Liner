# URFCO-01: exact Goedel-Dirichlet coding
ACRRO-08 offline CI 44920230319 and Lean CI 44920201206 passed.
For positive integer g, D_g(s)=sum_{p|g} v_p(g) exp(-s log p)
is a finite entire Dirichlet polynomial. Its negative derivative at
zero is log g by prime factorization. Exact reconstruction uses the
canonical prime-exponent tuple rather than numeric exp/log.
The empty tuple represents 1, not 0. Evaluation at integer s in
[-16,16] uses Fraction. Trial division is bounded to codes <=10^8;
not suitable for large proof codes and not a proof verifier.
Tests cover 10000 roundtrips, rational evaluations and invalid tuples.
The prime representation alone does not certify a logical proof.
Future URFCO stages must distinguish semantic zero from provability
and use independent certificate verification. No general halting
decision, classical Riemann hypothesis, or deployment claim.
