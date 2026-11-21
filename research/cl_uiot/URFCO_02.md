# URFCO-02: exact zero-point computation
URFCO-01 CI 44921323529 passed.
For nonnegative rational r_n, integer sigma>=2, let a_n=r_n/(1+r_n).
Exact prefix L=sum a_n/p_n^sigma. Since 0<=a_n<=1, the tail
is <= sum_{k>p_N} k^-sigma <= integral_{p_N}^infinity x^-sigma dx
=1/((sigma-1)*p_N^(sigma-1)). Hence [L,L+tail] encloses every
nonnegative continuation. Positive L proves nonzero. Zero prefix
returns UNKNOWN, never a universal zero certificate.
For the two-by-two example the scalar residual mu^2*(1+lambda^2)
vanishes iff mu=0 over rationals or reals; this is a specific
algebraic theorem, not a universal proof-search algorithm.
Tests cover exact tiny positive residual, 315 prefix bounds,
289 coefficient pairs and invalid domains. Standard library only.
No floating-point arithmetic, general halting oracle or physical
infinite computation claim. CI pending.
