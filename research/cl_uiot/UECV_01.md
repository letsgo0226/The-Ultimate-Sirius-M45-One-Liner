# UECV-01: independent identity decision path
UECS-08 offline CI 44925742711 passed; all eight UECS stage CIs passed.
A separate parser proves a conservative syntactic degree bound by
structural recursion and evaluates expressions directly with Fraction.
Agreement at d+1 distinct integers proves equality by the root bound.
No import of symbolic_algebra or proof_halting in the new checker.
Differential tests compare 578 cases, plus delayed witness and limits.
The degree bound may reject expressions accepted after cancellation
by normalization; UNKNOWN is not a disagreement in truth. Evaluation
has an 8192-bit intermediate cap, depth 32, 1024 nodes per expression,
degree 64. Shared Python runtime and Fraction remain trusted.
This is a second decision path, not a full independent certificate
checker or a formal refinement. Original API unchanged. CI pending.
No merge, deploy, or baseline change.
