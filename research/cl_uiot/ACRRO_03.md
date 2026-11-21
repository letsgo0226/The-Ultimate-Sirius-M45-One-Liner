# ACRRO-03: cross-dimensional reversible spectra
ACRRO-02 passed CI 44917086505. Split an integer signal on G_(n+1)
into blocks (a,b) on G_n, indexed by the new high bit.
With A=W_n a, B=W_n b, the butterfly gives W_(n+1)(a,b)=(A+B,A-B).
The inverse block mapping divides sum and difference by two.
Integer parity is required, and each recovered block spectrum must
also belong to the image of the integer Walsh transform.
Zero extension E(a)=(a,0) corresponds to spectral duplication (A,A).
Full split retains both blocks; projection alone loses information.
Cube Laplacian has block form [[L+I,-I],[-I,L+I]].
Tests cover 6561 ternary signals of length 8 and deterministic
Laplacian blocks through lower dimension 7. Length cap 4096.
No unbounded resource growth, physical singularity elimination,
or inversion of arbitrary irreversible computation. Lean pending.
CSGGO and USRCO Stirling remain pending. No merge or deployment.
