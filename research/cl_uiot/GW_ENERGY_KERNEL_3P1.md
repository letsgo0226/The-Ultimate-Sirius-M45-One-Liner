# TT gravitational-wave energy kernel

For the existing local polynomial TT waves f(t-z), g(t-z), compute K_ab = sum_ij partial_a h_ij partial_b h_ij = 2(f'^2+g'^2) k_a k_b, k=(1,0,0,-1). This kernel is symmetric, null-trace and divergence-free for this plane-wave family. K_00 is nonnegative for real profiles; K^03=K_00 describes the positive-z direction.

In units c=1, the leading Isaacson effective tensor in a suitable short-wavelength averaging regime is <K_ab>/(32 pi G_N). This prototype implements **only the unaveraged kernel**, not an averaging operator, general second-order Einstein tensor, physical local gravitational energy or backreaction. Polynomial profiles are local examples, not bounded high-frequency waves. An affine profile may have zero linearized curvature but nonzero kernel: this illustrates why the raw expression cannot be interpreted as gauge-invariant physical energy in arbitrary circumstances.

Seven regression tests check normalization of the kernel, flux signs, null trace and conservation for this family. No merge or deployment.
