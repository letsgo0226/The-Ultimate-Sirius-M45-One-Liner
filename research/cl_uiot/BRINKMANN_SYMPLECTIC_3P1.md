# Symplectic transverse Brinkmann evolution

Use canonical state z=(X,P_X,Y,P_Y), with momenta equal to u derivatives. J=diag(J2,J2), J2=[[0,1],[-1,0]]. H=(P_X²+P_Y²+K(u)(X²-Y²))/2 is the transverse Hamiltonian. Its generator A=J Hess(H) satisfies A^T J+J A=0. Differentiating F^T J F for the fundamental matrix F'=AF proves F^T J F=J for every finite interval, using F(s)=I. H need not be conserved: along solutions dH/du=K'(u)(X²-Y²)/2. This is a reduced Hamiltonian, not a physical gravitational energy density.

The code audits exact Taylor coefficients of the symplectic identity through finite order, using the existing geodesic jets. Finite truncations evaluated at nonzero time need not themselves be exactly symplectic. No global numerical symplectic integrator or quantum theory is claimed. No merge or deployment.
