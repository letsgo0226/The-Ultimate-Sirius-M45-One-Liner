# ACRRO-05: rational spectral pole regularization
ACRRO-04 passed CI 44917606509. On the n-cube let L=nI-A.
Walsh diagonalization gives eigenvalues 2|k|. For z off spectrum,
R(z)=(L-zI)^-1=sum_j P_j/(2j-z).
For lambda=2j, (lambda-z)R(z) extends at lambda as P_j.
For 0<|z-lambda|<=1, other eigenvalues are at distance >=1,
so the Euclidean error is <= |z-lambda| ||f||_2.
The projection alone is lossy; the complete labeled family
sums to f and reconstructs Lf via eigenvalue weighting.
Implementation uses exact Fraction arithmetic, integer input signals,
and inherited length cap 4096. Tests cover 81 ternary length-four
signals, orthogonality, decomposition and 16 rational pole approaches
on a length-eight signal. No claim of Schwarzschild curvature removal,
Riemann hypothesis, or arbitrary irreversible recovery.
Lean verification pending. No merge or deployment.
