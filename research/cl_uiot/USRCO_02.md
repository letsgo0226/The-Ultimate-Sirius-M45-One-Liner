# USRCO-02: singularity diagnostics
USRCO-01 passed CI 44913663902. In geometrized units G=c=1,
Schwarzschild Kretschmann scalar K=48 M^2/r^6 for r>0, M>0.
At r=2M it equals 3/(4 M^4). At r=0 the scalar diverges along
r=1/n. The diagnostic classifies these known cases; it is not a
general singularity classifier or a numerical spacetime solver.
The rescaled scalar r^6 K=48 M^2 and reciprocal 1/K extend finitely
to zero, but neither removes the original curvature divergence.
Kruskal extension of the horizon is a known geometric result,
not derived by this implementation. Exact rational tests check
the scalar formulas and projective reflection J T J = T^-1
on 288 homogeneous pairs. No proof of arbitrary program continuity,
physical singularity removal, or halting oracle. No deployment.
Lean checks and Stirling bounds remain pending.
