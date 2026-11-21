# URFCO-03: exact algebraic zero operator
URFCO-02 CI 44921498920 passed.
For known nonnegative rational c, Omega(s)=(s-1/2)^2+c
has roots 1/2 +/- i sqrt(c), simple for c>0 and a double
center root for c=0. The reflection s->1-s exchanges the
roots. Store rational real part, imaginary sign, rational
radicand and multiplicity, not a floating approximation.
Substitution checks real and radical coefficients exactly.
528 coefficient cases and 289 matrix parameter pairs, plus
tiny positive and invalid cases, are included in tests.
This polynomial surrogate is not the classical zeta or the
infinite cosh series. A zero finite prefix cannot be supplied
as a certified global c=0; this module assumes the given c
is exact. No universal halting or physical infinity claim.
CI pending. No merge or deployment.
