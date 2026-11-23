# UECV-02: dual certificate verification
UECV-01 CI 44925847764 passed. Added opt-in run_dual and verify_dual.
Require original certificate verification and independent AST decision
to agree on the verdict. For counterexamples independently evaluate the
specific witness in the original certificate, not merely the second
search result. Fail closed to UNKNOWN on rejection or resource limit.
Tests include 578 matching cases, simulated disagreement and UNKNOWN,
tampered witnesses and substituted propositions.
The two paths share Python and Fraction; this is not independent human
review or a formal kernel. Existing UECS API and baseline unchanged.
CI pending. No merge or deployment.
