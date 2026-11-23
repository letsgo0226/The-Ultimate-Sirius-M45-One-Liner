# UECS-04: exact involution polynomial calculus
UECS-03 CI 44923960300 passed.
For T^2=I, finite polynomial P(T)=aI+bT where a,b are sums
of even and odd coefficients respectively. This follows by reducing
powers and holds for bounded involutions on infinite-dimensional spaces
as a mathematical identity. Finite Python evaluation validates T^2=I;
independent Horner matrix evaluation checks the result. The direct-limit
prefix API reuses the URFCO-06 block operator and commutes with zero
padding, since I and T do. It does not materialize infinite vectors.
Tests cover 289 rational parameter pairs, inconsistent results,
float aliases, and 64 prefix embeddings. CI pending. Same polynomial
and matrix limits as earlier modules. No general operator identity
decision, Lean refinement, merge, deployment or baseline changes.
