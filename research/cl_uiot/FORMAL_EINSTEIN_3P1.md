# Formal finite-order Einstein tensor

For g=sum eps^n g_n, g_0=eta, compute inverse coefficients B_0=eta and B_n=-eta sum_{k=1}^n g_k B_{n-k}. All subsequent products use truncated Cauchy convolution. The connection, Ricci, scalar and Einstein tensors follow their ordinary coordinate formulas coefficient by coefficient. Exact rational spacetime polynomials are used. No factorial normalization.

Independent low-order checks compare previous modules. For g=(1+2 eps t)eta the exact G_00=3 eps²/(1+2 eps t)^2 supplies third and fourth coefficients -12t and 36t². The code computes coefficients for any finite input length; it does not solve arbitrary higher-order field equations, bound runtime or establish convergence of an infinite series. No merge or deployment.
