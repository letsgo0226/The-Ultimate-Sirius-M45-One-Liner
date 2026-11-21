# Local second-order TT backreaction correction

For the fixed polynomial TT plane-wave family, G2_ab=S(u) k_a k_b, u=t-z, k=(1,0,0,-1). The transverse isotropic correction j_11=j_22=q(u), all other entries zero, has G1_ab[j]=q''(u) k_a k_b. Construct q by integrating -S twice with q(0)=q'(0)=0. The code obtains S by evaluating G2_00 at x=y=z=0, then reconstructs q(t-z). Full component residual tests verify the ansatz for the selected examples.

This is a local perturbative particular solution, not a harmonic-gauge solver, a global boundary-value solution or a general backreaction operator. The integration constants are a chosen normalization, not physical initial data for all spacetime. No averaging or nonlinear continuation is asserted. No merge or deployment.
