# URFCO-07: restricted correspondence certificate
URFCO-06 CI 44922473124 passed.
For rational lambda,mu the fixed theorem relates zero residual,
mu=0, a double center root and proof halt for the instance.
The structured record binds parameters, exact residual, symbolic
roots, fixed tableau, state and prime representation of a theorem ID.
60 is an assigned theorem identifier, NOT an encoding of all proof
bytes. Its factorization is reversible but does not authenticate
the record. The checker recomputes instance fields independently
of the producer and uses the existing trusted tableau bridge rules.
It does not verify arbitrary theorems or the infinite direct-limit
construction; that construction has a separate mathematical proof
in URFCO_06.md. Zero residual does not encode unique parameters.
Tests cover 289 rational instances, seven inconsistent field edits
and tiny positive residuals. Consistency checking is not a signature;
coherent replacement with another valid instance is possible.
CI pending. Lean certification remains separate. No merge or deployment.
