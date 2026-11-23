# Linearized geodesic deviation

Using signature +--- and the existing curvature convention, a local inertial observer with zeroth-order four-velocity (1,0,0,0) sees spatial relative acceleration a^i = delta^{ik} R^(1)_0k0j X^j, for constant zeroth-order spatial separation X. In TT gauge this is -1/2 partial_t² h_ij X^j. A particular displacement is -h_ij X^j/2; add constant and linear-in-time terms to enforce initial data at the detector. The polynomial code retains spacetime coordinates symbolically; evaluate along a fixed background detector worldline. It neglects higher-order perturbations and finite-separation effects.

Seven tests cover both polarizations, longitudinal response, affine profiles, particular displacement and pure gauge. This is not a full numerical spacetime or detector simulation. No merge or deployment.

Run: python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
