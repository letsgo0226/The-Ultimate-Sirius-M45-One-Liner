# ACRRO-02: exact abelian Fourier operator
ACRRO-01 passed CI 44915331920. For G=(Z/2Z)^n, N=2^n,
W[k,x]=(-1)^popcount(k & x). Character orthogonality gives
W^2=N I and W^T W=N I. Inverse W/N is exact on integer spectra
in the image of W. Nonintegral inverse outputs are rejected.
Translation by g corresponds to multiplication by character(g).
Cube Laplacian L=nI-A satisfies W L=diag(2 popcount(k)) W.
Tests enumerate 3^8=6561 ternary signals on the 3-cube and
translation identities through dimension 6 on deterministic signals.
Fast butterfly uses O(N log N) integer operations, not constant
bit cost. Length capped at 4096 (dimension 12); integers arbitrary
precision. This is classical finite computation, not a quantum speedup
or arbitrary irreversible machine restoration. No deployment.
Cross-dimensional spectral embedding and Lean proofs pending.
