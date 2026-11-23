# URFCO-05: exact compatible inflation coefficients
URFCO-04 CI 44922133764 passed.
Given rational involutions T,S and standard embedding x->(x,0),
a compatible extension must have blocks [T,A;0,S].
It is involutive iff TA+AS=0.
All solutions are A=P(X)=(X-TXS)/2: substitution gives
TA+AS=0; conversely any solution satisfies TAS=-A, so P(A)=A.
P is an idempotent linear projection, not necessarily orthogonal.
Nonzero A maps new coordinates into old ones, not old into new.
Tests cover 1296 seed/matrix combinations, projection idempotence,
involution and embedding, plus nonzero rational coupling and invalids.
Exact Fraction arithmetic; matrix dimensions capped at 32.
This is a finite-dimensional theorem with arbitrary finite sizes
mathematically, not a proof of boundedness on a Hilbert completion.
CI pending; no merge or deployment.
