# M45-ST/75 — Relational Quantum Information-Gain Optimization

ST74 compared three resource-allocation policies. ST75 adds a fourth policy with an **explicit mathematical objective**: maximize the **approximate one-step expected reduction in posterior variance of the relational phase parameter** `theta`.

## Statistical model and decision objective

For the same ST69 relational event, `p(theta)=(1+sin(theta))/2`, and the detector-flipped science probability is `r=q+(1-2q)p(theta)`. Reference calibration outcomes are Bernoulli(`q`), and science outcomes are Bernoulli(`r`). The controller maintains **independent working Beta posteriors** for `q` and `r`:

- `q ~ Beta(1+k_q, 19+n_q-k_q)` (prior Beta(1,19)).
- `r ~ Beta(1+k_r, 1+n_r-k_r)` (prior Beta(1,1)).

For a Beta posterior with concentration `s=a+b` and variance `V=ab/[s^2(s+1)]`, the expected variance reduction after `b_new` additional Bernoulli observations is **exactly**

`Delta V = V * b_new/(s+b_new)`.

The policy maps these reductions into approximate phase-risk reduction via the **delta method**. With `p=(r-q)/(1-2q)`, the derivatives are

`d theta/d p = 1/sqrt(p(1-p))`,
`d p/d r = 1/(1-2q)`, and
`d p/d q = (2r-1)/(1-2q)^2`.

It compares the squared derivative times expected variance reduction for the calibration and science streams and chooses the larger. **This is a one-step local approximation, not an exact mutual-information optimizer.** The independent Beta working model does not enforce the physical constraints `q<1/2` and `q<=r<=1-q` everywhere. To keep derivatives finite, decision calculations clamp `q` to at most `0.49` and `p` to `[1e-6,1-1e-6]`; this is a numerical heuristic, not a posterior truncation.

## Paired policy benchmark

Under identical per-replication budgets and independent calibration/science Bernoulli streams, ST75 compares:

1. Balanced allocation.
2. Science-heavy allocation.
3. ST73 sensitivity-based adaptive allocation.
4. ST75 expected-posterior-risk allocation.

All policies consume **prefixes of the same pre-generated independent streams within each replication**. Metrics include mean trial count, interval width, target-hit fraction, empirical coverage, bias, RMSE and paired differences. No statistical superiority claim is made without repeated results and appropriate uncertainty analysis.

## Confidence guarantee versus Bayesian decision

The **allocation rule** is Bayesian and approximate; the **reported confidence intervals** are the conservative frequentist ST73 intervals, with `sqrt(log(4*budget/alpha)/(2*n))` radius for each stream. Under the stable independent Bernoulli model and a known reference bit, their simultaneous per-replication coverage is at least `1-alpha` even with adaptive allocation and optional stopping. This does not imply that the approximate Bayesian risk estimate is calibrated, that the policy is optimal, or that a particular Monte Carlo run must cover the true phase.

```sh
python3 -m unittest discover -s m45-st75 -p 'test_*.py'
python3 m45-st75/information_gain.py --theta 0.3 --flip 0.15 --budget 1200 --batch 50 --replications 100
```

**Limits:** no real quantum hardware, no general quantum reference-frame theorem, no autonomous scientific discovery, no model-misspecification robustness guarantee, no proven global optimality, and no formal between-policy significance test. CI and review pending.
