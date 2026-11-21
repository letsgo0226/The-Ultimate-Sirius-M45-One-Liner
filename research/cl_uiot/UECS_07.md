# UECS-07: restricted proof-halting decision procedure
UECS-06 Lean CI 44925053213 and offline CI 44925059065 passed.
For accepted rational polynomial expressions, normalize P-Q. Zero
gives an identity certificate; otherwise search integers 0..degree.
A nonzero degree d polynomial has at most d roots, so this terminates
with an exact counterexample. Unsupported syntax/resource limits give
UNKNOWN, which is not a proof or counterexample. The certificate binds
both original syntax codes, exact residual and optional witness.
Verifier recomputes residual and evaluates original sides separately;
it shares the trusted normalization code, not an independent formal
kernel. No general truth-tree engine or universal halting oracle.
Tests: 289 identities and 289 counterexamples, delayed witness at 12,
tampering and unsupported syntax. CI pending. No merge, deployment,
or baseline changes.
