# Recursive finite-order TT vacuum corrections

Starting from a local polynomial TT wave h1(u), u=t-z, compute the order-n Einstein coefficient with h_n initially zero. For the transverse plane-wave ansatz the source is S_n(u) k_a k_b. Choose h_n,11=h_n,22=q_n(u) with q_n''=-S_n and q_n(0)=q_n'(0)=0; other entries vanish. This uses the linearity of the dependence on the newest coefficient. At every step recompute every Einstein component at all retained orders and raise an error if any residual is nonzero.

The algorithm is conditional on the ansatz succeeding; the tests cover orders two through four. The chosen integration constants are normalization conditions. No general existence, convergence, global Lorentzian signature, arbitrary source solver or runtime bound is established. No merge or deployment.
