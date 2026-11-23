# UECS-03: exact symbolic polynomial interface
UECS-02 CI 44923358393 passed.
Expressions are tuple trees with rational literals, x, +, -, *.
Normalize to ascending exact rational coefficients, removing trailing
zeros except the canonical zero (0,). By uniqueness of polynomial
coefficients, equality of normal forms decides polynomial identity
for accepted expressions. Structural induction gives correctness of
the arithmetic rules; no Lean refinement proof yet.
Encode syntax using compact JSON and existing base-257 codec.
Reversible syntax encoding is distinct from semantic normalization;
different expressions may have identical normal forms.
Limits: depth 32, 1024 nodes, intermediate degree 64, literal 256
bits, coefficient 4096 bits, encoded bytes 4096. Rejected expressions
are unsupported, not false. No division, transcendental functions,
arbitrary symbolic identities or unsafe eval. Tests cover 289
rational binomial identities, roundtrips and malformed inputs.
CI pending. No merge, deployment or baseline modification.
