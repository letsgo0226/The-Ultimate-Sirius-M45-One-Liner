# UECV-05: bounded exact rational arithmetic
UECV-04 Python CI passed (44927328539); Lean failed (44927318798)
because real division lacks executable code. Marked uecvOmega
noncomputable in 29fb5b977e6665009bf078d3548f85b493ff24c0;
reverification pending. No theorem removed.
Added opt-in rational arithmetic with conservative pre-operation
bit bounds for unreduced numerators and denominators. Rejection
returns UNKNOWN, not a mathematical verdict. Cancellation could
make rejected operations small; conservatism is intentional.
Tests compare 1122 operations with Fraction and check limits/types.
This is not an OS memory/time sandbox; inputs already exist and
the API is not yet integrated into all existing computation paths.
CI pending. No merge, deployment or baseline change.
