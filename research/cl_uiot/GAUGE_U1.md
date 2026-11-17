# Infinitesimal local U(1) covariance: first-order toy model

A complex scalar field can be represented as a real doublet `phi=(phi_1,phi_2)`, with complex multiplication by `i` represented by `J=[[0,-1],[1,0]]`. Set `D_mu phi = partial_mu phi + q A_mu J phi` for a nonzero rational charge `q`.

For an infinitesimal *local* real gauge parameter `alpha(t,x)`, define

```text
delta phi = alpha J phi
delta A_mu = -(partial_mu alpha)/q
delta(D_mu phi) = alpha J (D_mu phi) + O(alpha²).
```

At first order the identity follows by the product rule and `J²=-I`; the derivative of alpha cancels the gauge-potential shift. The program represents alpha, A, and both components of phi by exact rational polynomials and verifies this first-order identity for test examples.

**Scope and caution:** This is an *infinitesimal*, classical, Abelian gauge transformation. It does not check finite local U(1) transformations, gauge-field curvature, Maxwell equations, a gauge-invariant action, quantum field theory, or unification. The field A is supplied, not dynamically determined. A general proof is written algebraically here, but tests are bounded and not machine-checked proof-assistant formalization.

The preceding free real scalar action is not by itself the minimally coupled complex-scalar action; that requires a separate new action and variations with respect to the gauge potential.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/gauge_u1_infinitesimal.py
```

This is research-only material in draft PR #67, with no merge, deployment, funds, or secret handling.
