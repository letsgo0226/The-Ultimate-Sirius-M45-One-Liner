# URFCO-04: restricted zero tableau
URFCO-03 CI 44921979763 passed. Negation of A iff B branches
into A and not B, or not A and B. Here A means mu^2(1+lambda^2)=0,
B means mu=0 over the reals. Two trusted algebraic bridge rules
close the branches: positivity of 1+lambda^2 and zero substitution.
Producer and checker are separate modules. Checker validates the
fixed branch proof, not arbitrary algebraic inference. HALT_PROOF
means the supplied rational instance has zero residual;
HALT_COUNTEREXAMPLE means it has nonzero residual, not that the
universal equivalence is false. 289 rational instances and malformed
certificates tested by CI (pending). No general tableau search or
halting oracle. Lean certification of bridge rules pending.
No merge or deployment.
