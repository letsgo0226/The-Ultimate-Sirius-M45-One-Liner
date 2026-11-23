# UECS-08: independent exact computation interface
UECS-07 offline CI 44925465251 passed.
Independent offline Python API integrates encoded polynomial identity
requests, involution matrix evaluation, and restricted correspondence
certificates. Identity results additionally expose sum of squared
residual coefficients and exact algebraic roots of (s-1/2)^2+energy.
Verification is relative to existing shared arithmetic/checker modules,
not an independent Lean kernel. UNKNOWN is not a truth verdict.
JSON reports use tagged hexadecimal integers and rational numerators/
denominators to avoid decimal conversion limits and floating point.
No network, autonomous execution, or baseline changes. This is an API,
not a CLI, general oracle, or physical hardware independence proof.
Tests cover 17 identity cases, operator validation, tiny residual,
certificate roundtrip and malformed requests. CI pending.
Open: full Lean l2 construction, Python refinement, independent review,
and stronger input resource isolation. No merge or deployment.
